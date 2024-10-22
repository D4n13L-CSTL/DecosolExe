from PyInstaller.utils.hooks import copy_metadata, collect_data_files

datas = copy_metadata('Babel')
datas += collect_data_files('babel')
