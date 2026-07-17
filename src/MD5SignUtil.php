<?php

/**
 * MD5 签名工具（对应 Java MD5SignUtil.getSign）
 *
 * 规则（与常见开放平台 MD5 签名一致）：
 * 1. 剔除 sign、空值、字节流/文件等参数，按参数名 ASCII 升序排序
 * 2. 拼成 key1=value1&key2=value2... 得到 stringA
 * 3. 拼接秘钥后做 MD5，默认：MD5(stringA + "&key=" + appSecret) 并转大写
 *
 * 若对接文档的秘钥拼接方式不同，可通过 $secretAppendMode 切换：
 * - key      : stringA + "&key=" + appSecret     （默认，微信/多数开放平台风格）
 * - raw      : stringA + appSecret
 * - amp      : stringA + "&" + appSecret
 * - appSecret: stringA + "&appSecret=" + appSecret
 */
class MD5SignUtil
{
    public const APPEND_KEY = 'key';
    public const APPEND_RAW = 'raw';
    public const APPEND_AMP = 'amp';
    public const APPEND_APP_SECRET = 'appSecret';

    /**
     * 生成签名
     *
     * @param array $params 请求参数（可含 sign，会被自动剔除）
     * @param string $appSecret 应用秘钥
     * @param string $secretAppendMode 秘钥拼接方式，见类常量
     * @param bool $upperCase 是否转大写，默认 true
     * @return string MD5 签名
     */
    public static function getSign(
        array $params,
        string $appSecret,
        string $secretAppendMode = self::APPEND_KEY,
        bool $upperCase = true
    ): string {
        $stringSignTemp = self::buildStringSignTemp($params, $appSecret, $secretAppendMode);
        $sign = md5($stringSignTemp);

        return $upperCase ? strtoupper($sign) : $sign;
    }

    /**
     * 生成待 MD5 的完整字符串（便于与 Java 侧对照调试）
     */
    public static function buildStringSignTemp(
        array $params,
        string $appSecret,
        string $secretAppendMode = self::APPEND_KEY
    ): string {
        $stringA = self::buildStringA($params);

        switch ($secretAppendMode) {
            case self::APPEND_RAW:
                return $stringA . $appSecret;
            case self::APPEND_AMP:
                return $stringA . '&' . $appSecret;
            case self::APPEND_APP_SECRET:
                return $stringA . '&appSecret=' . $appSecret;
            case self::APPEND_KEY:
            default:
                return $stringA . '&key=' . $appSecret;
        }
    }

    /**
     * 生成待签名字符串 stringA（不含秘钥）
     */
    public static function buildStringA(array $params): string
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

        return implode('&', $pairs);
    }
}
