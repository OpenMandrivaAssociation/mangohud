%define oname   MangoHud

Name:           mangohud
Version:        0.3.1
Release:        1
Summary:        A Vulkan and OpenGL overlay layer for monitoring FPS, temperatures, CPU/GPU load and more
Group:          Games/Arcade
License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
# Use tarball .xz only because in basic .tar.gz archive and in source code .tar.gz not all files available (missing submodules)
#Source0:        https://github.com/flightlessmango/MangoHud/releases/download/v%{version}/%{oname}-src-v%{version}.tar.xz
# Tarball not available with this release, so use source tar.gz and submodules.
Source0:        %{oname}-%{version}.tar.lz

BuildRequires: meson
BuildRequires: glslang
BuildRequires: glslang-devel
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(dri)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(x11)
BuildRequires: python3dist(mako)

Requires: vulkan-loader
Requires: %{_lib}vulkan1

Provides: bundled(ImGui) = 0.13.03.2020

%description
A Vulkan and OpenGL overlay layer for monitoring FPS, temperatures, CPU/GPU load and more.
A modification of the Mesa Vulkan overlay. Including GUI improvements, temperature reporting, and logging capabilities.

To enable the MangoHud overlay layer for 64bit Vulkan and OpenGL, run :
mangohud /path/to/app
Or
mangohud.x86 /path/to/app for 32bit OpenGL
For Steam games, you can add this as a launch option:
mangohud %command%
Or alternatively, add MANGOHUD=1 to your shell profile (Vulkan only).

%prep
%autosetup -p1 -n %{oname}-%{version}

%build

%meson -Duse_system_vulkan=enabled
%meson_build

%install
%meson_install

%files
%doc README.md bin/%{oname}.conf LICENSE MangoHud.conf.example
%{_bindir}/mangohud
%{_libdir}/mangohud/lib%{oname}.so
%{_datadir}/vulkan/implicit_layer.d/%{oname}.*.json
