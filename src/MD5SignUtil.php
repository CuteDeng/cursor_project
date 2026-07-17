<?php

/**
 * MD5 签名工具（对应 Java MD5SignUtil.getSign）
 *
 * 规则：
 * 1. 剔除 sign、空值、字节流/文件等参数，按参数名 ASCII 升序排序
 * 2. 拼成 key1=value1&key2=value2... 待签名字符串
 * 3. 末尾追加 &key={appSecret}，再做 MD5，结果转大写
 */
class MD5SignUtil
{
    /**
     * 生成签名
     *
     * @param array $params 请求参数（可含 sign，会被自动剔除）
     * @param string $appSecret 应用秘钥
     * @return string 大写 MD5 签名
     */
    public static function getSign(array $params, string $appSecret): string
    {
        $filtered = [];

        foreach ($params as $key => $value) {
            if ($key === 'sign') {
                continue;
            }
            // 跳过资源句柄、文件上传对象等字节类型参数
            if (is_resource($value) || $value instanceof SplFileInfo) {
                continue;
            }
            if ($value === null || $value === '') {
                continue;
            }
            // 数组/对象转 JSON 字符串参与签名（一般业务为扁平参数）
            if (is_array($value) || is_object($value)) {
                $value = json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
            }

            $filtered[(string) $key] = (string) $value;
        }

        ksort($filtered, SORT_STRING);

        $pairs = [];
        foreach ($filtered as $key => $value) {
            $pairs[] = $key . '=' . $value;
        }

        $stringA = implode('&', $pairs);
        $stringSignTemp = $stringA . '&key=' . $appSecret;

        return strtoupper(md5($stringSignTemp));
    }
}
