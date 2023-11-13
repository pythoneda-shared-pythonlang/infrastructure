# Infrastructure

Shared kernel for infrastructure layers.

## How to declare it in your flake

Check the latest tag of the artifact repository: https://github.com/pythoneda-shared-pythoneda/infrastructure-artifact/tags, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-pythoneda-infrastructure = {
      [optional follows]
      url =
        "github:pythoneda-shared-pythoneda/infrastructure-artifact/[version]?dir=infrastructure";
    };
  };
  outputs = [..]
};
```

Should you use another PythonEDA modules, you might want to pin those also used by this project. The same applies to nixos/nixpkgs and flake-utils.
The Nix flake is under the `infrastructure` folder of https://github.com/pythoneda-shared-pythoneda/infrastructure-artifact.

