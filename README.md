# Infrastructure

Shared library for infrastructure layers.

## How to declare it in your flake

Check the latest tag of the definition repository: <https://github.com/pythoneda-shared-pythonlang-def/infrastructure/tags>, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-pythonlang-infrastructure = {
      [optional follows]
      url =
        "github:pythoneda-shared-pythonlang-def/infrastructure/[version]";
    };
  };
  outputs = [..]
};
```

Should you use another PythonEDA modules, you might want to pin those also used by this project. The same applies to nixos/nixpkgs and flake-utils.
The Nix flake is hosted in its [https://github.com/pythoneda-shared-pythonlang-def/infrastructure](definition "definition") repository.

