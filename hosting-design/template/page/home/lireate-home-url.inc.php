<?php
/**
 * Абсолютный https-URL для ссылок главной (без http://$cit_in).
 */
if (!function_exists('lireate_home_abs_url')) {
    function lireate_home_abs_url($path)
    {
        $path = is_string($path) ? $path : '';
        if ($path === '') {
            return '/';
        }
        if ($path[0] !== '/') {
            $path = '/' . $path;
        }
        $base = '';
        if (isset($cit_in) && is_string($cit_in) && $cit_in !== '') {
            $base = preg_replace('#^http:#i', 'https:', $cit_in);
            $base = rtrim($base, '/');
        } elseif (!empty($_SERVER['HTTP_HOST'])) {
            $host = preg_replace('/[^a-zA-Z0-9.\-:]/', '', (string) $_SERVER['HTTP_HOST']);
            if ($host !== '') {
                $base = 'https://' . $host;
            }
        }
        if ($base === '') {
            return $path;
        }
        return $base . $path;
    }
}
