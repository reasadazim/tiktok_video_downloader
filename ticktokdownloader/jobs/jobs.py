import os
import shutil

from ..models import Files


def delete_downloads():
    queryset_files = Files.objects.filter(deleted=0)

    for file in queryset_files:

        file_path_nowatermark = file.path_nowatermark
        file_path_nowatermark = file_path_nowatermark[5:]
        file_path_nowatermark= f'public/static{file_path_nowatermark}'

        # Instaloader creates a directory same as profile_name. So delete that after successful DP scrap
        if os.path.exists(f'{file_path_nowatermark}'):
            os.remove(f'{file_path_nowatermark}')
            update = Files.objects.get(uid=file.uid)
            update.delete()

        file_path_watermark = file.path_watermark
        file_path_watermark = file_path_watermark[5:]
        file_path_watermark= f'public/static{file_path_watermark}'

        # Instaloader creates a directory same as profile_name. So delete that after successful DP scrap
        if os.path.exists(f'{file_path_watermark}'):
            os.remove(f'{file_path_watermark}')
