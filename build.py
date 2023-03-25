import datetime
import os
import random
import shutil
import subprocess

import PyInstaller.__main__


def build_rust():
	if os.path.isfile(".\\lib\\rust_2048.pyd"):
		os.remove(".\\lib\\rust_2048.pyd")

	subprocess.run(["cargo", "clean"], cwd=".\\rust_2048", stdin=None, stdout=None, stderr=None, input=None, capture_output=False,
	               timeout=None, check=True, shell=False, env=None, universal_newlines=False, errors=None,
	               text=None)

	subprocess.run(["cargo", "build", "--release"], cwd=".\\rust_2048", stdin=None, stdout=None, stderr=None, input=None, capture_output=False,
	               timeout=None, check=True, shell=True, env=None, universal_newlines=False, errors=None,
	               text=None)

	# rename file
	os.rename(".\\rust_2048\\target\\release\\rust_2048.dll", ".\\rust_2048\\target\\release\\rust_2048.pyd")

	# copy file
	shutil.copyfile(".\\rust_2048\\target\\release\\rust_2048.pyd", ".\\lib\\rust_2048.pyd")

	subprocess.run(["cargo", "clean"], cwd=".\\rust_2048", stdin=None, stdout=None, stderr=None, input=None,
	               capture_output=False,
	               timeout=None, check=True, shell=False, env=None, universal_newlines=False, errors=None,
	               text=None)

def build(name, console, onefile, uac_admin, icon, upx, files, folders, compile_rust):
	if compile_rust:
		build_rust()

	work_path = "build"
	while os.path.isdir(work_path):
		work_path = f"build_{random.randint(1, 1_000_000_000)}"
	work_path = os.path.join(os.path.abspath("."), work_path)

	result_path = os.path.abspath(".")

	run_list = ['main.py',
	            '--noconfirm',
	            '--clean',
	            '--name', f"{name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}",
	            '--workpath', work_path,
	            '--specpath', work_path,
	            '--distpath', result_path]

	if console:
		run_list.append("--console")
	else:
		run_list.append("--noconsole")

	if onefile:
		run_list.append("--onefile")
	else:
		run_list.append("--onedir")

	if uac_admin:
		run_list.append("--uac-admin")

	if icon != "":
		icon_path = os.path.join(os.path.abspath("."), icon)
		if not os.path.isfile(icon_path):
			raise Exception("Invalid icon!")
		else:
			run_list.extend(('--icon', icon_path))

	if upx != "":
		if not os.path.isfile(upx):
			raise Exception("Invalid UPX!")
		else:
			upx_path = os.path.join(os.path.abspath("."), os.path.dirname(upx))
			run_list.extend(('--upx-dir', upx_path))

	for file in files:
		if os.path.isfile(os.path.join(os.path.abspath("."), file)):
			run_list.extend(('--add-data', f'{os.path.join(os.path.abspath("."), file)};{os.path.dirname(file)}'))
		else:
			raise Exception("Invalid file!")

	for folder in folders:
		if os.path.isdir(folder):
			for walk in os.walk(folder, followlinks=False):
				for file in walk[2]:
					if os.path.isfile(os.path.join(walk[0], file)):
						run_list.extend(('--add-data', f'{os.path.join(os.path.abspath("."), os.path.join(walk[0], file))};{os.path.dirname(os.path.join(walk[0], file))}'))
					else:
						raise Exception("Invalid folder!")
		else:
			raise Exception("Invalid folder!")

	PyInstaller.__main__.run(run_list)
	shutil.rmtree(path=work_path, ignore_errors=True)

def main():
	name = "2048-v7.0.0"
	console = False
	onefile = True
	uac_admin = False
	icon = "data\\2048-icon.ico"
	upx = "data\\upx-win64\\upx.exe"
	files = [icon]
	folders = []

	# compile Rust code
	# needs to be True for every platform except Windows x64 (as it is precompiled for it)
	# Rust needs to be installed and added to PATH as well as cargo
	compile_rust = True

	build(name, console, onefile, uac_admin, icon, upx, files, folders, compile_rust)


if __name__ == '__main__':
	main()
