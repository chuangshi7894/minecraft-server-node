import os
import json
import subprocess

# ========== 配置区 ==========
minecraft_dir = os.path.join(os.getcwd(), ".minecraft")
java_path = "javaw"          # 如果 java 不在 PATH 中，写完整路径，如 "C:/Java/bin/javaw.exe"
memory = "4G"
version = "1.20.1"           # 改成你已安装的版本
username = "Steve"
# ===========================

# 1. 读取版本 JSON
version_json_path = os.path.join(minecraft_dir, "versions", version, f"{version}.json")
with open(version_json_path, "r", encoding="utf-8") as f:
    version_info = json.load(f)

# 2. 构建 classpath（libraries + 版本 jar）
libraries = []
for lib in version_info["libraries"]:
    artifact = lib.get("downloads", {}).get("artifact")
    if artifact and "path" in artifact:
        lib_path = os.path.join(minecraft_dir, "libraries", artifact["path"])
        if os.path.exists(lib_path):
            libraries.append(lib_path)

libraries.append(os.path.join(minecraft_dir, "versions", version, f"{version}.jar"))
classpath = os.pathsep.join(libraries)

# 3. natives 路径（Windows 下通常长这样，视版本而定）
natives_dir = os.path.join(minecraft_dir, "versions", version, "natives-windows-x86_64")
if not os.path.exists(natives_dir):
    # 有些旧版本 natives 在版本文件夹下直接叫 natives
    alt = os.path.join(minecraft_dir, "versions", version, "natives")
    if os.path.exists(alt):
        natives_dir = alt

# 4. 拼接启动命令
command = [
    java_path,
    f"-Xmx{memory}",
    "-Xms512M",
    f"-Djava.library.path={natives_dir}",
    "-cp", classpath,
    version_info["mainClass"],
    "--username", username,
    "--version", version,
    "--gameDir", minecraft_dir,
    "--assetsDir", os.path.join(minecraft_dir, "assets"),
    "--assetIndex", version_info.get("assetIndex", {}).get("id", version),
    "--accessToken", "0",          # 离线模式随便填
    "--userType", "legacy",
]

# 5. 启动
print("正在启动 Minecraft...")
subprocess.Popen(command, cwd=minecraft_dir)