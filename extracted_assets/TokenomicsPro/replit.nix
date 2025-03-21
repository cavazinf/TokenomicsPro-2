{pkgs}: {
  deps = [
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.unzip
    pkgs.glibcLocales
  ];
}
