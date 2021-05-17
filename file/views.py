from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from account.models import WorkGroup
from file.forms import FileForm, PathForm
from file.models import FileSystem, Path, File
from mail.models import Message

User = get_user_model()


class FileView(LoginRequiredMixin, View):
    def get(self, request):
        group = get_object_or_404(WorkGroup, pk=request.user.groupID)
        if FileSystem.objects.filter(group=group):
            info = group.files
            return HttpResponseRedirect('%d' % info.root_path_id)
        else:
            root = Path(name='群文件', groupID=group.id, is_root=True)
            root.save()
            info = FileSystem(group=group, root_path_id=root.id, file_count=0, file_size_count=0)
            info.save()
        root = get_object_or_404(Path, pk=info.root_path_id)
        path = Path.objects.filter(parent=root.id)
        files = File.objects.filter(parent=root.id)
        return render(request, 'file/file.html', {'info': info, 'path': path, 'files': files})


class FolderView(LoginRequiredMixin, View):
    def get(self, request, path_id):
        path = get_object_or_404(Path, pk=path_id)
        if request.user.groupID == path.groupID:
            children = Path.objects.filter(parent=path_id)
            files = File.objects.filter(parent=path_id)
            group = get_object_or_404(WorkGroup, pk=request.user.groupID)
            info = get_object_or_404(FileSystem, group=group)
            return render(request, 'file/file.html',
                          {'path': path, 'info': info, 'children': children, 'files': files})
        else:
            return HttpResponse('无权限访问')


class DownloadView(LoginRequiredMixin, View):
    def get(self, request, file_id):
        file = get_object_or_404(File, pk=file_id)
        return FileResponse(file.file)


class UploadView(LoginRequiredMixin, View):
    def post(self, request, path_id):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            saved_file = File.objects.create(name=file.name, file=file, parent=path_id, owner=request.user.email,
                                             groupID=request.user.groupID)
            saved_file.save()
            info = get_object_or_404(WorkGroup, id=request.user.groupID).files
            info.file_count += 1
            info.file_size_count += file.size
            info.save()
            # 向组内其他人发送通知
            for user in User.objects.filter(groupID=request.user.groupID):
                if user != request.user:
                    Message(owner=user, type=3, item_id=saved_file.id, content=saved_file.name,
                            involved=request.user).save()
            return redirect('file:main')
        else:
            return HttpResponse('上传文件失败')


class NewFolderView(LoginRequiredMixin, View):
    def post(self, request, path_id):
        form = PathForm(request.POST)
        if form.is_valid():
            new_path = Path(parent=path_id, name=form.cleaned_data['folder'], groupID=request.user.groupID)
            new_path.save()
            return redirect('file:main')
        else:
            return HttpResponse('新建文件夹失败')


class FileDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST.get('fileID')
        file = get_object_or_404(File, pk=id)
        info = get_object_or_404(WorkGroup, pk=request.user.groupID).files
        info.file_count -= 1
        info.file_size_count -= file.file.size
        file.delete()
        return redirect('file:main')


class FileDetailView(LoginRequiredMixin, View):
    def get(self, request, file_id):
        file = get_object_or_404(File, id=file_id)
        return FileResponse(file.file)
