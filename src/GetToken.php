<?php

require_once __DIR__ . '/MD5SignUtil.php';

/**
 * H5 刷脸认证初始化（对应 Java GetToken）
 */
class GetToken
{
    /** @var string 测试环境地址 */
    public const TEST_URL = 'http://testyqt.easysign.cn:8028/APIService/api/v2/face/getToken';

    private string $appId;
    private string $appSecret;
    private string $version;
    private string $apiUrl;
    private int $timeout;

    public function __construct(
        string $appId,
        string $appSecret,
        string $version = '1.0',
        string $apiUrl = self::TEST_URL,
        int $timeout = 60
    ) {
        $this->appId = $appId;
        $this->appSecret = $appSecret;
        $this->version = $version;
        $this->apiUrl = $apiUrl;
        $this->timeout = $timeout;
    }

    /**
     * 调用 getToken 接口
     *
     * @param array $bizParams 业务参数，例如 name / idCard / cardType / returnUrl / authType
     * @return array{http_code:int, body:string, data:?array}
     */
    public function request(array $bizParams): array
    {
        $body = array_merge($bizParams, [
            'appId' => $this->appId,
            'version' => $this->version,
            'timestamp' => (string) (int) (microtime(true) * 1000),
            'nonce' => $this->generateNonce(),
        ]);

        $body['sign'] = MD5SignUtil::getSign($body, $this->appSecret);

        return $this->postJson($this->apiUrl, $body);
    }

    /**
     * 生成 8 位随机整数（不足左侧补 0）
     */
    private function generateNonce(): string
    {
        return sprintf('%08d', random_int(0, 99999999));
    }

    /**
     * POST JSON
     */
    private function postJson(string $url, array $body): array
    {
        $payload = json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $payload,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CONNECTTIMEOUT => $this->timeout,
            CURLOPT_TIMEOUT => $this->timeout,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json; charset=utf-8',
                'Content-Length: ' . strlen($payload),
            ],
        ]);

        $responseBody = curl_exec($ch);
        $httpCode = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);

        if ($responseBody === false) {
            throw new RuntimeException('请求失败: ' . $error);
        }

        $decoded = json_decode($responseBody, true);

        return [
            'http_code' => $httpCode,
            'body' => $responseBody,
            'data' => is_array($decoded) ? $decoded : null,
            'request' => $body,
        ];
    }
}

// CLI 直接运行示例：php src/GetToken.php
if (PHP_SAPI === 'cli' && realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) {
    // 敏感信息建议从环境变量读取
    $appId = getenv('EASYSIGN_APP_ID') ?: '474jNjIGdD7o';
    $appSecret = getenv('EASYSIGN_APP_SECRET') ?: 'd086196caf3be536a02da3c438c238f0d0e9ead6';

    $client = new GetToken($appId, $appSecret);

    $result = $client->request([
        'name' => '张三',
        'idCard' => '111111111',
        'cardType' => '1',
        'returnUrl' => 'http://testyqt.esa2000.com:8080/UUMS/sys/reg/authSuccess',
        'authType' => '1',
        // 'provideAuthPage' => '2',
    ]);

    echo "request sign = " . $result['request']['sign'] . PHP_EOL;
    echo "response = " . $result['body'] . PHP_EOL;
}
