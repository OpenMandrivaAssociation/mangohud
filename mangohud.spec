%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define oname   MangoHud

Name:           mangohud
Version:        0.6.7
Release:        1
Summary:        A Vulkan and OpenGL overlay layer for monitoring FPS, temperatures, CPU/GPU load and more
Group:          Tools/Monitiring/Overlay
License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        https://github.com/flightlessmango/MangoHud/releases/download/v%{version}/%{oname}-v%{version}-Source.tar.xz

%if %{with compat32}
BuildRequires:	devel(libGLX_mesa)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libvulkan)
%endif

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
BuildRequires: pkgconfig(wayland-client)
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
%setup -n %{oname}-v%{version} -q
#setup -n %{oname}-%{version} -q -D -T -a1
#patch -p1
#mv imgui-20200503/* modules/ImGui/src/

%build
%if %{with compat32}

%meson32 \
	-Duse_system_vulkan=enabled \
	-Dwith_x11=enabled \
	-Dwith_wayland=enabled
%endif


%meson \
	-Duse_system_vulkan=enabled \
	-Dwith_x11=enabled \
	-Dwith_wayland=enabled
# error duplicate symbol dlsym if compiled with enabled	
#	-Dwith_dlsym=enabled

%if %{with compat32}
%ninja_build -C build32
%endif

%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

%files
%doc README.md bin/%{oname}.conf LICENSE
%{_datadir}/doc/mangohud/MangoHud.conf.example
%{_bindir}/mangohud
%{_libdir}/mangohud/lib%{oname}.so
%{_libdir}/mangohud/lib%{oname}_dlsym.so
%{_datadir}/vulkan/implicit_layer.d/*
%{_mandir}/man1/mangohud.1.*
