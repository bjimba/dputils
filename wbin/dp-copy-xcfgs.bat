@echo off

rem copy all xcfgs in this directory to devel\dpcompare, with marker

for %%f in (*.xcfg) do (
  copy %%f %my_home%\devel\dpcompare\%%~nf.%1.xcfg
)
