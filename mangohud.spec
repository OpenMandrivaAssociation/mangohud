%define oname   MangoHud

Name:           mangohud
Version:        0.3.5
Release:        2
Summary:        A Vulkan and OpenGL overlay layer for monitoring FPS, temperatures, CPU/GPU load and more
Group:          Games/Arcade
License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        https://github.com/flightlessmango/MangoHud/archive/v%{version}/%{oname}-%{version}.tar.gz
# Submodule should be downloaded from here:
#Source1:        https://github.com/flightlessmango/ImGui/archive/1f02d240b38f445abb0381ade0867752d5d2bc7b/ImGui-1f02d240b38f445abb0381ade0867752d5d2bc7b.tar.gz
Source1:	imgui-20200503.tar.gz

BuildRequires: cmake
BuildRequires: meson
BuildRequires: glslang
BuildRequires: glslang-devel
#FIXME
BuildRequires: %{_lib}XNVCtrl-devel
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(dri)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(x11)
BuildRequires: python3dist(mako)

Requires: vulkan-loader
Requires: %{_lib}vulkan1

Provides: bundled(ImGui) = 0.20200313

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
#autosetup -p1 -n %{oname}-%{version}
	
%setup -n %{oname}-%{version} -q
%setup -n %{oname}-%{version} -q -D -T -a1
mv imgui-20200503/* modules/ImGui/src/

%build

%meson -Duse_system_vulkan=enabled
%meson_build

%install
%meson_install

%files
%doc README.md bin/%{oname}.conf LICENSE MangoHud.conf.example
%ifnarch %{ix86} %{arm}
%{_bindir}/mangohud
%else
%{_bindir}/mangohud.x86
%endif
%{_libdir}/mangohud/lib%{oname}.so
%{_libdir}/mangohud/lib%{oname}_dlsym.so
%{_datadir}/vulkan/implicit_layer.d/%{oname}.*.json
