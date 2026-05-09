{
  description = "Audio File Scanner & Player - scans directories for audio files and plays them";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Define the complete python environment required for all scripts
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          tkinter
          pygame
          mutagen
          pillow
        ]);

        # Package the whole source directory so relative imports work
        mp3AutorunPkg = pkgs.stdenv.mkDerivation {
          name = "mp3-autorun";
          src = ./.;
          buildInputs = [ pythonEnv ];
          installPhase = ''
            mkdir -p $out/bin
            mkdir -p $out/share/mp3-autorun
            
            # Copy all python files to the share directory
            cp -r ./*.py $out/share/mp3-autorun/
            cp -r ./player $out/share/mp3-autorun/
            
            # Create a wrapper for the player application
            cat > $out/bin/mp3-player <<EOF
            #!/bin/sh
            exec ${pythonEnv}/bin/python $out/share/mp3-autorun/player/player.py "\$@"
            EOF
            chmod +x $out/bin/mp3-player

            # Create a wrapper for the scanner tool
            cat > $out/bin/mp3-scanner <<EOF
            #!/bin/sh
            exec ${pythonEnv}/bin/python $out/share/mp3-autorun/scanner.py "\$@"
            EOF
            chmod +x $out/bin/mp3-scanner
          '';
        };
      in {
        # Expose the packaged applications
        packages.default = mp3AutorunPkg;

        # Define apps so you can run 'nix run' directly
        apps = {
          default = {
            type = "app";
            program = "${mp3AutorunPkg}/bin/mp3-player";
          };
          player = {
            type = "app";
            program = "${mp3AutorunPkg}/bin/mp3-player";
          };
          scanner = {
            type = "app";
            program = "${mp3AutorunPkg}/bin/mp3-scanner";
          };
        };

        # Provide a complete development shell for working on the code
        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ];
          
          shellHook = ''
            echo "MP3Autorun Development Shell Loaded"
            echo "Available commands in this shell: python, python3"
            echo "Installed modules: tkinter, pygame, mutagen, pillow"
          '';
        };
      });
}
