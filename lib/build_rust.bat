@echo off
cd ..
IF EXIST .\lib\rust_2048.pyd (
    DEL /F .\lib\rust_2048.pyd
)
cd .\rust_2048
cargo clean
cargo build --release
ren .\target\release\rust_2048.dll rust_2048.pyd
copy .\target\release\rust_2048.pyd ..\lib\rust_2048.pyd
cargo clean
cd ..
cd .\lib
