from django.core.exceptions import ValidationError

MAX_VIDEO_SIZE_MB = 20

def validate_video_size(file):
    limit = MAX_VIDEO_SIZE_MB * 1024 * 1024
    if file.size > limit:
        raise ValidationError(f"O vídeo não pode passar de {MAX_VIDEO_SIZE_MB}MB.")