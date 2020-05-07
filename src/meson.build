pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'thumbdrives')
gnome = import('gnome')

gnome.compile_resources('thumbdrives',
  'thumbdrives.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'thumbdrives.in',
  output: 'thumbdrives',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

thumbdrives_sources = [
  '__init__.py',
  'main.py',
  'vdisk.py',
  'window.py',
]

install_data(thumbdrives_sources, install_dir: moduledir)
install_data('pk-thumbdrive-action.sh', install_dir: get_option('bindir'), install_mode: 'rwxr-xr-x', rename: ['pk-thumbdrive-action'])
