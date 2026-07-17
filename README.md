# H5 刷脸 getToken（PHP）

将 Java `GetToken` + `MD5SignUtil.getSign` 封装为 PHP 版本。

## 签名规则

1. **筛选并排序**：排除 `sign`、空值、文件/字节流参数；按参数名 ASCII 升序排序  
2. **拼接**：`key1=value1&key2=value2...` 得到待签名字符串 `stringA`  
3. **MD5 签名**：对 `stringA + "&key=" + appSecret` 做 MD5，结果转大写

> 若对接方文档要求秘钥拼接方式不同（例如直接追加 `appSecret`，或 `&appSecret=`），只需改 `MD5SignUtil::getSign` 中拼接那一行。

## 文件

| 文件 | 说明 |
|------|------|
| `src/MD5SignUtil.php` | 签名工具 |
| `src/GetToken.php` | 调用 `/api/v2/face/getToken` |
| `examples/sign_demo.php` | 本地验签演示 |

## 用法

```php
require_once __DIR__ . '/src/GetToken.php';

$client = new GetToken(
    getenv('EASYSIGN_APP_ID') ?: 'your_app_id',
    getenv('EASYSIGN_APP_SECRET') ?: 'your_app_secret'
);

$result = $client->request([
    'name' => '张三',
    'idCard' => '111111111',
    'cardType' => '1',
    'returnUrl' => 'https://your.domain/callback',
    'authType' => '1',
]);

echo $result['body'];
```

## 本地验证签名

```bash
php examples/sign_demo.php
```

## 发起真实请求（需网络可达测试环境）

```bash
export EASYSIGN_APP_ID=474jNjIGdD7o
export EASYSIGN_APP_SECRET=your_secret
php src/GetToken.php
```
