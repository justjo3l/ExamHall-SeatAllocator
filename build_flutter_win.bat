rmdir /s /q EHSA_V3\bin\data && del /q EHSA_V3\bin\ehsa_frontend.exe del /q EHSA_V3\bin\flutter_windows.dll
cd ehsa_frontend && flutter build windows && cd ../ && move ehsa_frontend\build\windows\runner\Release\data EHSA_V3\bin && move ehsa_frontend\build\windows\runner\Release\ehsa_frontend.exe EHSA_V3\bin && move ehsa_frontend\build\windows\runner\Release\flutter_windows.dll EHSA_V3\bin
