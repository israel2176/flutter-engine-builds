# flutter-engine-builds

Public build farm for Flutter engines with extra root certificates (`libflutter.so`).


- **Build**: Actions → *Build Flutter Engine (extra roots)* → inputs `engine_hash`, `android_cpu`.
- **Output**: release `engine-<cpu>-<engine_hash>` with `libflutter-<cpu>-<engine_hash>.so`.
- **Download**: `gh release download engine-arm64-<hash> --repo israel2176/flutter-engine-builds -p '*.so'`
