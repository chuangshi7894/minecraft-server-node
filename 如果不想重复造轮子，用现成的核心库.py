from easy_mc_launcher import EasyLauncher, SettingsManager

launcher = EasyLauncher()
settings = SettingsManager()
settings.set("username", "Player")
settings.set("ram_max", "4G")

# 自动安装 Fabric 并返回版本名
fabric_version = launcher.install_fabric("1.20.1")
launcher.launch(fabric_version, settings)