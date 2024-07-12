# Talisman configuration settings
hsts = {
    'max-age': 31536000,
    'includeSubDomains': True
}

csp = {
  'default-src': [
		'\'self\'',
    '\'unsafe-inline\''
	],
  'form-action': [
    '\'self\''
  ],
  'object-src': [
    '\'none\''
  ],
  'frame-ancestors': [
    '\'none\''
  ],
  'style-src': [
    '\'self\'',
    '\'unsafe-inline\'',
    'https://use.fontawesome.com/',
    'https://fonts.googleapis.com/',
    'https://fonts.gstatic.com/',
    'https://cdnjs.cloudflare.com/',
  ],
  'img-src': [
    '\'self\'',
    'data:',
    'blob:',
    'https://cdn.buymeacoffee.com/'
  ],
  'script-src': [
    '\'self\'',
    '\'unsafe-inline\'',
    'https://cdnjs.buymeacoffee.com/',
  ],
  'font-src': [
    '\'self\'',
    'data:',
    'https://fonts.gstatic.com/',
    'https://fonts.googleapis.com/',
    'https://use.fontawesome.com/',
    'https://cdnjs.cloudflare.com/',

  ],
}

permissions_policy = {
  'geolocation': '()',
  'microphone': '()',
  'accelerometer': '()',
  'ambient-light-sensor': '()',
  'autoplay': '()',
  'battery': '()',
  'camera': '()',
  'display-capture': '()',
  'document-domain': '()',
  'encrypted-media': '()',
  'fullscreen': '()',
  'gamepad': '()',
  'gyroscope': '()',
  'layout-animations': '\'self\'',
  'legacy-image-formats': '\'self\'',
  'magnetometer': '()',
  'midi': '()',
  'oversized-images': '\'self\'',
  'payment': '()',
  'picture-in-picture': '()',
  'publickey-credentials-get': '()',
  'speaker-selection': '()',
  'sync-xhr': '\'self\'',
  'unoptimized-images': '\'self\'',
  'unsized-media': '\'self\'',
  'usb': '()',
  'screen-wake-lock': '()',
  'web-share': '()',
  'xr-spatial-tracking': '()'
}

# You can either export each setting individually or wrap them in a dictionary
talisman_settings = {
    'force_https': False,
    'session_cookie_secure': True,
    'content_security_policy': csp,
    'strict_transport_security': hsts,
    'referrer_policy': 'no-referrer',
    'content_type_nosniff': True,
    'xss_protection': True,
    'frame_options': 'deny',
    'permited_cross_domain_policies': 'none',
    'clear_site_data': ['cache', 'cookies', 'storage'],
    'cross_origin_embedder_policy': 'require-corp',
    'cross_origin_opener_policy': 'same-origin',
    'cross_origin_resource_policy': 'same-origin',
    'cache_control': ['no-store', 'max-age=0'],
    'permissions_policy': permissions_policy
}