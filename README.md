## 技术选型

Framework: Django + Django REST Framework
DataBase: MySQL + Redis

## 项目思路

- Router 路由

- Auth 全局认证

- Throttle 节流

- View 视图 (GenericViewSet - ModelMixin - RestFul)

- Serilizer 校验（is_valid)

- Filter 过滤

- 业务逻辑

  - DataBase(MySQL, Django ORM)
  - Cache(Redis)

- Pagination 分页

- Serilizer 序列化（serializer.data）

## 功能实现

- 登录
- 注册
- 我的话题

  - 我的话题列表
  - 创建话题
  - 修改话题
  - 删除话题（逻辑删除）

- 我的资讯

  - 创建资讯（5 分钟创建一个，需要根据用户限流） 问题 1：5/h 2/m； 问题 2：成功后，下次再创建；
  - 文本（你问我答、42 区、挨踢 1024、段子）
  - 图片（图片、你问我答、42 区、挨踢 1024、段子）
  - 连接（图片、你问我答、42 区、挨踢 1024、段子）
    注意：创建时默认自己做 1 个推荐。
  - 我的资讯列表

- 资讯首页

  - 时间倒序，读取已审核通过的资讯
  - 加载更多，分页处理
  - 支持传入参数，查询各分区资讯：图片、你问我答、42 区、挨踢 1024、段子 ?zone=2

- 推荐

  - 推荐
  - 取消推荐
  - 我的推荐列表

- 收藏
  - 收藏 or 取消收藏
  - 我的收藏列表
