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
$stringA = MD5SignUtil::buildStringA($params);
$stringSignTemp = MD5SignUtil::buildStringSignTemp($params, $appSecret);

echo "stringA         = {$stringA}" . PHP_EOL;
echo "stringSignTemp  = {$stringSignTemp}" . PHP_EOL;
echo "sign            = {$sign}" . PHP_EOL;

$expect = strtoupper(md5($stringA . '&key=' . $appSecret));
echo "expect          = {$expect}" . PHP_EOL;
echo ($sign === $expect ? "OK: sign matched" : "FAIL: sign mismatch") . PHP_EOL;
