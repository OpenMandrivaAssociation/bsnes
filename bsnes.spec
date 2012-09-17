%define		vernumber 091

Name:		bsnes
Version:	0.%{vernumber}
Release:	%mkrel 1
Summary:	A multi-system emulator (SNES, NES, GB, GBA, GBC)
License:	GPLv3
Group:		Emulators
URL:		http://byuu.org/bsnes/
Source0:	http://bsnes.googlecode.com/files/%{name}_v%{vernumber}-source.tar.xz
Patch0:		bsnes-088-datapath.patch
Patch1:		bsnes-088-gtkfix.patch
Patch2:		bsnes-088-makefile.patch
BuildRequires:	libao-devel
BuildRequires:	libxv-devel
BuildRequires:	openal-devel
BuildRequires:	gtk+2-devel
BuildRequires:	qt4-devel
BuildRequires:	SDL-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	libgomp-devel
BuildRequires:	gcc >= 4.5
Requires:	%{name}-binary = %{EVRD}

%description
The purpose of BSNES is a bit different from other emulators.
It focuses on accuracy, debugging functionality, and clean code.
The emulator does not focus on things that would hinder accuracy.
This includes speed and game-specific hacks for compatibility.
As a result, the minimum system requirements for bsnes are very high.

The emulator itself was not derived from any existing emulator source
code, such as SNES9x. It was written from scratch by myself.
Any similarities to other emulators are merely coincidental.

BSNES also has Game Boy (GB, GBC and GBA) and NES emulation support.

Note that you will need the GBA BIOS image to use this. There will not
be any high-level emulation of the BIOS functions for obvious reasons.
Name the file "bios.rom", and place it inside the
"/var/games/bsnes/Game Boy Advance.sys/" directory.

Important! Most likely you won't be able to run SNES ROMs until you
"purify" them with snespurify utility.

Warning! BSNES is still not very stable and may crash with some video
settings, filters/shaders and hardware combination.

%files
%defattr(-,root,root)
%{_datadir}/pixmaps/%{name}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/shaders
%{_datadir}/%{name}/cheats.xml
%{_datadir}/%{name}/shaders/*.shader
%{_libdir}/%{name}/filters/*.filter
%{_var}/games/%{name}

#----------------------------------------------------------------------------

%package -n %{name}-qt4-compatibility
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-qt4-compatibility
BSNES binary compiled with Qt4/compatibility profile.

%files -n %{name}-qt4-compatibility
%defattr(-,root,root)
%{_gamesbindir}/%{name}-qt4-compatibility
%{_datadir}/applications/%{name}-qt4-compatibility.desktop

#----------------------------------------------------------------------------

%package -n %{name}-gtk-compatibility
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-gtk-compatibility
BSNES binary compiled with GTK/compatibility profile.

%files -n %{name}-gtk-compatibility
%defattr(-,root,root)
%{_gamesbindir}/%{name}-gtk-compatibility
%{_datadir}/applications/%{name}-gtk-compatibility.desktop

#----------------------------------------------------------------------------

%package -n %{name}-qt4-accuracy
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-qt4-accuracy
BSNES binary compiled with Qt4/accuracy profile.

%files -n %{name}-qt4-accuracy
%defattr(-,root,root)
%{_gamesbindir}/%{name}-qt4-accuracy
%{_datadir}/applications/%{name}-qt4-accuracy.desktop

#----------------------------------------------------------------------------

%package -n %{name}-gtk-accuracy
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-gtk-accuracy
BSNES binary compiled with GTK/accuracy profile.

%files -n %{name}-gtk-accuracy
%defattr(-,root,root)
%{_gamesbindir}/%{name}-gtk-accuracy
%{_datadir}/applications/%{name}-gtk-accuracy.desktop

#----------------------------------------------------------------------------

%package -n %{name}-qt4-performance
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-qt4-performance
BSNES binary compiled with Qt4/performance profile.

%files -n %{name}-qt4-performance
%defattr(-,root,root)
%{_gamesbindir}/%{name}-qt4-performance
%{_datadir}/applications/%{name}-qt4-performance.desktop

#----------------------------------------------------------------------------

%package -n %{name}-gtk-performance
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary = %{EVRD}

%description -n %{name}-gtk-performance
BSNES binary compiled with GTK/performance profile.

%files -n %{name}-gtk-performance
%defattr(-,root,root)
%{_gamesbindir}/%{name}-gtk-performance
%{_datadir}/applications/%{name}-gtk-performance.desktop

#----------------------------------------------------------------------------

%prep
%setup -qn %{name}_v%{vernumber}-source
# %patch0 -p1
# %patch1 -p1
# %patch2 -p1

%build
pushd %{name}

%if %{mdvver} > 201100
%__perl -pi -e "s/Q_MOC_OUTPUT_REVISION != 62/Q_MOC_OUTPUT_REVISION != 63/g" phoenix/qt/platform.moc
%endif

export CFLAGS="%{optflags}"

%__mkdir build

%make compiler=gcc phoenix=qt profile=compatibility
%__mv out/%{name} build/%{name}-qt4-compatibility
%__make clean

%make compiler=gcc phoenix=gtk profile=compatibility
%__mv out/%{name} build/%{name}-gtk-compatibility
%__make clean

%make compiler=gcc phoenix=qt profile=accuracy
%__mv out/%{name} build/%{name}-qt4-accuracy
%__make clean

%make compiler=gcc phoenix=gtk profile=accuracy
%__mv out/%{name} build/%{name}-gtk-accuracy
%__make clean

%make compiler=gcc phoenix=gtk profile=performance
%__mv out/%{name} build/%{name}-gtk-performance
%__make clean

%make compiler=gcc phoenix=qt profile=performance
%__mv out/%{name} build/%{name}-qt4-performance

popd

pushd snesfilter
%make compiler=gcc
popd

%install
%__rm -rf %{buildroot}

%__mkdir_p %{buildroot}%{_gamesbindir}
%__mkdir_p %{buildroot}%{_datadir}/applications
%__mkdir_p %{buildroot}%{_libdir}/%{name}/filters
%__mkdir_p %{buildroot}%{_datadir}/%{name}/shaders
%__mkdir_p %{buildroot}%{_datadir}/pixmaps

pushd %{name}

#install icon
%__install -m 644 data/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

#install cheats
%__install -m 644 data/cheats.xml %{buildroot}%{_datadir}/%{name}/cheats.xml

#install binaries
%__install -m 755 build/%{name}-qt4-compatibility %{buildroot}%{_gamesbindir}/%{name}-qt4-compatibility
%__install -m 755 build/%{name}-gtk-compatibility %{buildroot}%{_gamesbindir}/%{name}-gtk-compatibility
%__install -m 755 build/%{name}-qt4-accuracy %{buildroot}%{_gamesbindir}/%{name}-qt4-accuracy
%__install -m 755 build/%{name}-gtk-accuracy %{buildroot}%{_gamesbindir}/%{name}-gtk-accuracy
%__install -m 755 build/%{name}-qt4-performance %{buildroot}%{_gamesbindir}/%{name}-qt4-performance
%__install -m 755 build/%{name}-gtk-performance %{buildroot}%{_gamesbindir}/%{name}-gtk-performance

#install profiles
%__mkdir_p %{buildroot}%{_var}/games/%{name}
%__cp -r profile/* %{buildroot}%{_var}/games/%{name}/
%__chmod 777 -R %{buildroot}%{_var}/games/%{name}
find %{buildroot}%{_var}/games/%{name} -type f -exec chmod 666 {} \;

popd

#install shaders
%__install -m 644 snesshader/*.OpenGL.shader %{buildroot}%{_datadir}/%{name}/shaders/

#install filters
%__install -m 755 snesfilter/out/*.filter %{buildroot}%{_libdir}/%{name}/filters/

#install XDG menu entries
%__cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-compatibility.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (Qt4/Compatibility)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-qt4-compatibility
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Qt;Game;Emulator;
EOF

%__cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-compatibility.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (GTK/Compatibility)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-gtk-compatibility
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=GTK;Game;Emulator;
EOF

%__cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-accuracy.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (Qt4/Accuracy)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-qt4-accuracy
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Qt;Game;Emulator;
EOF

%__cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-accuracy.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (GTK/Accuracy)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-gtk-accuracy
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=GTK;Game;Emulator;
EOF

%__cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-performance.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (Qt4/Performance)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-qt4-performance
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=Qt;Game;Emulator;
EOF

%__cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-performance.desktop << EOF
[Desktop Entry]
Version=1.0
Name=BSNES (GTK/Performance)
Comment=SNES Emulator
Comment[ru]=Эмулятор SNES
Exec=%{name}-gtk-performance
Icon=%{_datadir}/pixmaps/%{name}.png
Terminal=false
Type=Application
Categories=GTK;Game;Emulator;
EOF

%clean
%__rm -rf %{buildroot}

