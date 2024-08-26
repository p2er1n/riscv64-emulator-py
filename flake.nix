{
  description = "riscv64 emulator written in python";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }: {

    packages.x86_64-linux.default = let
      pkgs = nixpkgs.legacyPackages."x86_64-linux";
    in
      pkgs.mkShell {
        nativeBuildInputs = with pkgs; [ python3 ];
      };
  };
}
