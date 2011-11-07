%define vernumber 084
%define name	bsnes
%define version 0.%{vernumber}
%define release %mkrel 1

Summary:	Super Nintendo Entertainment System (SNES) Emulator
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv3
Group:		Emulators
Source0:	%{name}_v%{vernumber}-source.tar.bz2
Patch0:		bsnes-083-datapath.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	libao-devel
BuildRequires:	libxv-devel
BuildRequires:	openal-devel
BuildRequires:	gtk+2-devel
BuildRequires:	qt4-devel
BuildRequires:	SDL-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	libgomp-devel
BuildRequires:	gcc >= 4.5
Requires:	%{name}-binary

%description
The purpose of BSNES is a bit different from other emulators.
It focuses on accuracy, debugging functionality, and clean code.
The emulator does not focus on things that would hinder accuracy.
This includes speed and game-specific hacks for compatibility.
As a result, the minimum system requirements for bsnes are very high.

The emulator itself was not derived from any existing emulator source
code, such as SNES9x. It was written from scratch by myself.
Any similarities to other emulators are merely coincidental.

BSNES also has Game Boy and NES emulation support (not very complete yet).

Important! Most likely you won't be able to run ROMs until you "purify"
them with snespurify utility.

Warning! BSNES is still not very stable and may crash with some video
settings, filters/shaders and hardware combination.

%files
%defattr(-,root,root)
%{_datadir}/pixmaps/%{name}.png
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/shaders
%{_datadir}/%{name}/cheats.bml
%{_datadir}/%{name}/shaders/*.shader
%{_libdir}/%{name}/filters/*.filter

#----------------------------------------------------------------------------

%package -n %{name}-qt4-compatibility
Summary:	Super Nintendo Entertainment System (SNES) Emulator
License:	GPLv3
Group:		Emulators
Requires:	%{name}
Provides:	%{name}-binary

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
Provides:	%{name}-binary

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
Provides:	%{name}-binary

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
Provides:	%{name}-binary

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
Provides:	%{name}-binary

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
Provides:	%{name}-binary

%description -n %{name}-gtk-performance
BSNES binary compiled with GTK/performance profile.

%files -n %{name}-gtk-performance
%defattr(-,root,root)
%{_gamesbindir}/%{name}-gtk-performance
%{_datadir}/applications/%{name}-gtk-performance.desktop

#----------------------------------------------------------------------------

%prep
%setup -c -qn %{name}_v%{vernumber}-source
%patch0 -p1

%build
pushd %{name}

%if %{mdvver} > 201100
%__perl -pi -e "s/Q_MOC_OUTPUT_REVISION != 62/Q_MOC_OUTPUT_REVISION != 63/g" phoenix/qt/platform.moc
%endif

%__mkdir build

%make compiler=gcc phoenix=qt profile=compatibility

mv out/%{name} build/%{name}-qt4-compatibility

make clean

%make compiler=gcc phoenix=gtk profile=compatibility

mv out/%{name} build/%{name}-gtk-compatibility

make clean

%make compiler=gcc phoenix=qt profile=accuracy

mv out/%{name} build/%{name}-qt4-accuracy

make clean

%make compiler=gcc phoenix=gtk profile=accuracy

mv out/%{name} build/%{name}-gtk-accuracy

make clean

%make compiler=gcc phoenix=gtk profile=performance

mv out/%{name} build/%{name}-gtk-performance

make clean

%make compiler=gcc phoenix=qt profile=performance

mv out/%{name} build/%{name}-qt4-performance

popd

pushd snesfilter

%make compiler=gcc

popd

sed -i "s/g++-4.5/g++/" snespurify/cc-gtk.sh

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%__mkdir -p %{buildroot}%{_gamesbindir}
%__mkdir -p %{buildroot}%{_datadir}/applications
%__mkdir -p %{buildroot}%{_libdir}/%{name}/filters
%__mkdir -p %{buildroot}%{_datadir}/%{name}/shaders
%__mkdir -p %{buildroot}%{_datadir}/pixmaps

pushd %{name}

#install icon
%__install -m 644 data/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

#install cheats
%__install -m 644 data/cheats.bml %{buildroot}%{_datadir}/%{name}/cheats.bml

#install binaries
%__install -m 755 build/%{name}-qt4-compatibility %{buildroot}%{_gamesbindir}/%{name}-qt4-compatibility
%__install -m 755 build/%{name}-gtk-compatibility %{buildroot}%{_gamesbindir}/%{name}-gtk-compatibility
%__install -m 755 build/%{name}-qt4-accuracy %{buildroot}%{_gamesbindir}/%{name}-qt4-accuracy
%__install -m 755 build/%{name}-gtk-accuracy %{buildroot}%{_gamesbindir}/%{name}-gtk-accuracy
%__install -m 755 build/%{name}-qt4-performance %{buildroot}%{_gamesbindir}/%{name}-qt4-performance
%__install -m 755 build/%{name}-gtk-performance %{buildroot}%{_gamesbindir}/%{name}-gtk-performance

popd

#install shaders
%__install -m 644 snesshader/*.OpenGL.shader %{buildroot}%{_datadir}/%{name}/shaders/

#install filters
%__install -m 755 snesfilter/out/*.filter %{buildroot}%{_libdir}/%{name}/filters/


#install XDG menu entries
cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-compatibility.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-compatibility.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-accuracy.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-accuracy.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/%{name}-qt4-performance.desktop << EOF
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

cat > %{buildroot}%{_datadir}/applications/%{name}-gtk-performance.desktop << EOF
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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

