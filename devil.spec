%define oname DevIL
%define major 1
%define libIL %mklibname IL %{major}
%define libILU %mklibname ILU %{major}
%define libILUT %mklibname ILUT %{major}
%define devname %mklibname %{name} -d
%define resildevname %mklibname resil -d

Summary:	Open source image library
Name:		devil
# We need to outnumber resil
# (previous fork -- ahead in version numbers but
# far behind in Linux support)
Epoch:		1
Version:	1.8.0
Release:	8
License:	LGPLv2+
Group:		System/Libraries
Url:		http://openil.sourceforge.net/
Source0:	http://downloads.sourceforge.net/openil/%{oname}-%{version}.tar.gz
Patch0:		DevIL-1.8.0-sonames.patch
Patch1:		DevIL-1.8.0-compile.patch
Patch2:		DevIL-jasper-3.0.6.patch
Patch3:		DevIL-1.8-clang16.patch

BuildRequires:	file
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libmng)
BuildRequires:	tiff-devel
BuildRequires:	ungif-devel
BuildRequires:	pkgconfig(allegro)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(zlib)

%description
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package 	utils
Summary:	Tools provided by %{oname}
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
%rename resil-utils

%description	utils
This package contains tools provided by %{oname}.

%package -n %{libIL}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Obsoletes:	%{_lib}devil1 < %{EVRD}

%description -n	%{libIL}
This package contains the shared library for %{oname}.

%package -n %{libILU}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Conflicts:	%{_lib}devil1 < %{EVRD}

%description -n	%{libILU}
This package contains the shared library for %{oname}.

%package -n %{libILUT}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Conflicts:	%{_lib}devil1 < %{EVRD}

%description -n	%{libILUT}
This package contains the shared library for %{oname}.

%package -n %{devname}
Summary:	Development headers and libraries for writing programs using %{oname}
Group:		Development/C
Requires:	%{libIL} = %{EVRD}
Requires:	%{libILU} = %{EVRD}
Requires:	%{libILUT} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	resil-devel < %{EVRD}
%define __requires_exclude 'devel\\(liballeg.*'
%rename %{resildevname}

%description -n	%{devname}
Development headers and libraries for writing programs using %{oname}.

%prep
%autosetup -n DevIL -p1

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%if "%_lib" != "lib"
find . -name CMakeLists.txt |xargs sed -i -e 's,DESTINATION lib,DESTINATION %_lib,g'
%endif

mkdir DevIL/build
cd DevIL
%cmake -G Ninja \
	-DIL_USE_DXTC_NVIDIA:BOOL=OFF

%build
cd DevIL
%ninja -C build

%install
cd DevIL
%ninja_install -C build

%files utils
%{_bindir}/ilur

%files -n %{libIL}
%{_libdir}/libIL.so.%{major}*

%files -n %{libILU}
%{_libdir}/libILU.so.%{major}*

%files -n %{libILUT}
%{_libdir}/libILUT.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/IL
