<?php

/**
 * 签名算法演示（不发网络请求）
 *
 * 运行：php examples/sign_demo.php
 */

require_once __DIR__ . '/../src/MD5SignUtil.php';

$appSecret = 'd086196caf3be536a02da3c438c238f0d0e9ead6';

$params = [
    'name' => '张三',
    'idCard' => '111111111',
    'cardType' => '1',
    'returnUrl' => 'http://testyqt.esa2000.com:8080/UUMS/sys/reg/authSuccess',
    'authType' => '1',
    'appId' => '474jNjIGdD7o',
    'version' => '1.0',
    'timestamp' => '1710000000000',
    'nonce' => '12345678',
    'sign' => 'should-be-ignored',
    'emptyField' => '',
];

$sign = MD5SignUtil::getSign($params, $appSecret);

echo "sign = {$sign}" . PHP_EOL;

// 手工复核：过滤 → 排序 → 拼接 → 追加 &key=secret → MD5 大写
$manual = [
    'appId' => '474jNjIGdD7o',
    'authType' => '1',
    'cardType' => '1',
    'idCard' => '111111111',
    'name' => '张三',
    'nonce' => '12345678',
    'returnUrl' => 'http://testyqt.esa2000.com:8080/UUMS/sys/reg/authSuccess',
    'timestamp' => '1710000000000',
    'version' => '1.0',
];
ksort($manual, SORT_STRING);
$pairs = [];
foreach ($manual as $k => $v) {
    $pairs[] = "{$k}={$v}";
}
$stringA = implode('&', $pairs);
$stringSignTemp = $stringA . '&key=' . $appSecret;
$expect = strtoupper(md5($stringSignTemp));

echo "stringA = {$stringA}" . PHP_EOL;
echo "expect  = {$expect}" . PHP_EOL;
echo ($sign === $expect ? "OK: sign matched" : "FAIL: sign mismatch") . PHP_EOL;
