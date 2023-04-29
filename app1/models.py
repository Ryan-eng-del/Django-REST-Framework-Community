from django.db import models

# Create your models here.


class DeleteModel(models.Model):
    deleted = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        abstract: True


class UserInfo(DeleteModel):
    STATUS_CHOICES = ((1, "激活"), (2, "禁用"))
    username = models.CharField(max_length=32, verbose_name="用户名")
    phone = models.CharField(max_length=32, db_index=True, verbose_name="手机号")
    password = models.CharField(max_length=64, verbose_name="密码")
    token = models.CharField(max_length=64, verbose_name="token", null=True)
    token_expires = models.DateTimeField(verbose_name="有效期", null=True)
    status = models.IntegerField(
        verbose_name="状态", choices=STATUS_CHOICES, default=1)
    create_datetime = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "user_info"
        indexes = [
            models.Index(
                fields=['username', "password"], name='idx_name_pwd')
        ]


class Topic(DeleteModel):
    title = models.CharField(verbose_name="话题", max_length=16, db_index=True)
    is_hot = models.BooleanField(verbose_name="热门话题", default=False)
    user = models.ForeignKey(
        to="UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)


class News(DeleteModel):
    '''新闻资讯'''
    zone_choices = ((1, "42区"), (2, "段子"), (3, "图片"),
                    (4, "挨踢1024"), (5, "你问我答"))
    zone = models.IntegerField(verbose_name="专区", choices=zone_choices)

    title = models.CharField(verbose_name="文字", max_length=150)
    url = models.CharField(
        verbose_name="链接", max_length=200, null=True, blank=True)
    create_datetime = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)

    status_choice = (
        (1, "待审核"),
        (2, "已通过"),
        (3, "未通过"),
    )

    status = models.IntegerField(
        verbose_name="状态", choices=status_choice, default=1)
        
    # xxxxx?xxxxxx.png,xxxxxxxx.jeg
    image = models.TextField(
        verbose_name="图片地址", help_text="逗号分割", null=True, blank=True)

    collect_count = models.IntegerField(verbose_name="收藏数", default=0)
    recommend_count = models.IntegerField(verbose_name="推荐数", default=0)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    user = models.ForeignKey(
        to="UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    topic_id = models.ForeignKey(
        verbose_name="话题", to="Topic", on_delete=models.CASCADE, null=True, blank=True)


class Collect(models.Model):
    """ 收藏 """
    news = models.ForeignKey(
        verbose_name="资讯", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)

    class Meta:
        # unique_together = [['news', 'user']]
        constraints = [
            models.UniqueConstraint(
                fields=['news', 'user'], name='uni_collect_news_user')
        ]


class Recommend(models.Model):
    """ 推荐 """
    news = models.ForeignKey(
        verbose_name="资讯", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['news', 'user'], name='uni_recommend_news_user')
        ]


class Comment(models.Model):
    """ 评论表 """
    news = models.ForeignKey(
        verbose_name="资讯", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(
        verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="内容", max_length=150)

    depth = models.IntegerField(verbose_name="深度", default=0)

    root = models.ForeignKey(verbose_name="根评论", to="Comment", related_name="descendant", on_delete=models.CASCADE,
                             null=True, blank=True)

    reply = models.ForeignKey(verbose_name="回复", to="Comment", related_name="reply_list", on_delete=models.CASCADE,
                              null=True, blank=True)

    create_datetime = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)

    # 针对根评论
    descendant_update_datetime = models.DateTimeField(
        verbose_name="后代更新时间", auto_now_add=True)
