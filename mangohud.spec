%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define lib32name libmangohud

%define oname   MangoHud

Name:           mangohud
Version:        0.7.2
Release:        1
Summary:        A Vulkan and OpenGL overlay layer for monitoring FPS, temperatures, CPU/GPU load and more
Group:          Tools/Monitiring/Overlay
License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        https://github.com/flightlessmango/MangoHud/releases/download/v%{version}/%{oname}-v%{version}-Source.tar.xz

%if %{with compat32}
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libGLX_mesa)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-server)
BuildRequires:	devel(libvulkan)
BuildRequires:	devel(libxkbcommon-x11)
BuildRequires:	libstdc++6
%endif

BuildRequires: git
BuildRequires: appstream
BuildRequires: cmake
BuildRequires: meson
BuildRequires: glslang
BuildRequires: glslang-devel
BuildRequires: vulkan-headers
BuildRequires: stdc++-devel
BuildRequires: stdc++-static-devel
#FIXME
BuildRequires: %{_lib}XNVCtrl-devel
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(dri)
BuildRequires: pkgconfig(nlohmann_json)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(spdlog)
BuildRequires: python3dist(mako)
BuildRequires: pkgconfig(xkbcommon-x11)

Requires: vulkan-loader
Requires: %{_lib}vulkan1
Recommends: %{lib32name}  = %{EVRD}
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

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared library for %{name} (32-bit)
Group:		System/Libraries
Requires:	libvulkan1

%description -n %{lib32name}
32-bit Vulkan and OpenGL overlay layer for monitoring FPS, temperatures, CPU/GPU load and more.
%endif

%prep	
%setup -n %{oname}-v0.7.1 -q
#setup -n %{oname}-%{version} -q -D -T -a1
#patch -p1
#mv imgui-20200503/* modules/ImGui/src/

%build
%if %{with compat32}

%meson32 \
	-Dwith_x11=enabled \
	-Dwith_wayland=enabled \
	-Dtests=disabled
%endif


%meson \
	-Dwith_x11=enabled \
	-Dwith_wayland=enabled \
	-Duse_system_spdlog=enabled \
	-Dtests=disabled
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
%doc README.md LICENSE
%doc %{_datadir}/doc/mangohud/presets.conf.example
%{_datadir}/doc/mangohud/MangoHud.conf.example
%{_bindir}/mangohud
%{_bindir}/mangoplot
%{_libdir}/mangohud/lib%{oname}.so
%{_libdir}/mangohud/lib%{oname}_dlsym.so
%{_libdir}/mangohud/libMangoHud_opengl.so
%{_datadir}/vulkan/implicit_layer.d/*
%{_datadir}/metainfo/io.github.flightlessmango.mangohud.metainfo.xml
%{_mandir}/man1/mangohud.1.*
%{_iconsdir}/hicolor/scalable/apps/io.github.flightlessmango.mangohud.svg

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/mangohud/libMangoHud.so
%{_prefix}/lib/mangohud/libMangoHud_dlsym.so
%{_prefix}/lib/mangohud/libMangoHud_opengl.so
%endif
