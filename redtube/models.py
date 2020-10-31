from django.db import models

from redtube import api

bn = dict(blank=True, null=True)

class Pornstar(models.Model):
    pornstar_id = models.PositiveIntegerField(primary_key=True)
    link = models.URLField(max_length=200)
    small_thumb_url = models.URLField(max_length=200, **bn)

    name = models.CharField(max_length=100)
    videos = models.PositiveSmallIntegerField(**bn)

    image_url = models.URLField(max_length=200, **bn)
    astrology = models.CharField(max_length=20, **bn)
    height = models.PositiveSmallIntegerField(**bn)
    weight = models.PositiveSmallIntegerField(**bn)

    rank = models.PositiveIntegerField(**bn)
    subscribers = models.PositiveIntegerField(**bn)
    views = models.PositiveIntegerField(**bn)

    ethnicity = models.CharField(max_length=20, **bn)
    hair_color = models.CharField(max_length=20, **bn)
    cup_size = models.CharField(max_length=5, **bn)
    date_of_birth = models.DateField(**bn)
    years_active = models.CharField(max_length=50, **bn)
    
    birth_place = models.CharField(max_length=200, **bn)
    tattoos = models.CharField(max_length=300, **bn)
    piercings = models.CharField(max_length=300, **bn)

    measurements = models.CharField(max_length=40, **bn)
    background = models.CharField(max_length=40, **bn)
    breast_type = models.CharField(max_length=20, **bn)
    performer_aka = models.CharField(max_length=200, **bn)
    bio = models.TextField(**bn)

    def __str__(self):
        return self.name

    @classmethod
    def sync_all_pornstars(cls):
        for page_number in range(1, 200):
            res = api.get_pornstars(page_number)
            if res is None:
                break
            for i in res:
                cls.from_json(i)


    def sync_all_unknown_pornstars(cls):
        for i in cls.objects.filter(image_url__isnull=True):
            i.update()


    @classmethod
    def from_json(cls, d):
        class_fields, data_fields = set(field.name for field in cls._meta.get_fields()), set(d.keys())
        p, _ = cls.objects.update_or_create(pornstar_id=d["pornstar_id"], defaults={k: d[k] for k in class_fields & data_fields})
        return p

    
    def update(self):
        res = api.get_pornstar(self.link)
        for video in res.get("most_viewed_videos", []):
            v = Video.from_json(video)
            _, _ = PornstarVideos.objects.get_or_create(pornstar_id=res["pornstar_id"], video=v)

        for similar_ps_id in res.get("similar_ps", []):
            _, _ = Similar.objects.get_or_create(pornstar_id=res["pornstar_id"], similar_to=similar_ps_id)

        return Pornstar.from_json(res)


class Similar(models.Model):
    pornstar = models.ForeignKey(Pornstar, on_delete=models.CASCADE)
    similar_to = models.PositiveIntegerField()


class Video(models.Model):
    video_id = models.PositiveIntegerField(primary_key=True)
    link = models.URLField(max_length=100)
    title = models.CharField(max_length=200)
    views = models.PositiveIntegerField()
    like_prc = models.PositiveSmallIntegerField()
    duration_sec = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    @classmethod
    def from_json(cls, d):
        class_fields, data_fields = set(field.name for field in cls._meta.get_fields()), set(d.keys())
        p, _ = cls.objects.update_or_create(video_id=d["video_id"], defaults={k: d[k] for k in class_fields & data_fields})
        return p


class PornstarVideo(models.Model):
    pornstar = models.ForeignKey(Pornstar, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
