# A puppet config to setup a webserver
package { 'nginx':
  ensure => 'installed',
}

file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared',
  '/data/web_static/releases/test']:
  ensure  => 'directory',
  owner   => 'Horbital1140',
  group   => 'Horbital1140',
  mode    => '0755',
  recurse => true,
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'Horbital1140',
  group  => 'Horbital1140',
  force  => true,
}

exec { 'add_location_to_nginx_config':
  command   => "/bin/sed -i \"/server_name _;/a\\        location /hbnb_static/ {alias /data/web_static/current/;}\"",
  path      => '/usr/bin:/usr/sbin:/bin:/sbin',
  provider  => 'shell',
  logoutput => false,
  require   => Package['nginx'],
  notify    => Service['nginx'],
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => Package['nginx'],
}
