##%define _disable_ld_no_undefined	1

%define	oname DevIL

%define	major 1
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d
%define	staticname	%mklibname %{name} -s -d

Summary:	Open source image library
Name:		devil
Version:	1.7.8
Release:	%mkrel 5
License:	LGPLv2+
Group:		System/Libraries
URL:		http://openil.sourceforge.net/
Source0:	http://downloads.sourceforge.net/openil/%{oname}-%{version}.tar.gz
Patch0:		devil-1.7.8-CVE-2009-3994.patch
Patch1:		devil-1.7.8-libpng15.patch
BuildRequires:	zlib-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	SDL-devel
BuildRequires:	png-devel
BuildRequires:	lcms-devel
BuildRequires:	mng-devel
BuildRequires:	mesaglu-devel
BuildRequires:	allegro-devel
BuildRequires:	ungif-devel
BuildRequires:	libtool
BuildRequires:	jasper-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	file

%description
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package -n %{libname}
Summary:	Libraries needed for programs using %{oname}
Group:		System/Libraries
Provides:	lib%{name}
Provides:	%{name}

%description -n	%{libname}
DevIL is an Open Source image library whose distribution is done under the
terms of the GNU LGPL license.
DevIL offers you a simple way to implement loading, manipulating, filtering,
converting, displaying, saving from/to several different image formats in your
own project.

%package -n %{develname}
Summary:	Development headers and libraries for writing programs using %{oname}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	allegro-devel
%if %{mdvver} >= 201200
%define __noautoreq 'devel\\(liballeg.*'
%else
%define	_requires_exceptions	devel(liballeg.*
%endif
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}devil1-devel

%description -n	%{develname}
Development headers and libraries for writing programs using %{oname}.

%package -n %{staticname}
Summary:	Static library for %{oname}
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%{_lib}devil1-static-devel

%description -n %{staticname}
Static library for %{oname}.

%package 	utils
Summary:	Tools provided by %{oname}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-utils = %{version}-%{release}

%description	utils
This package contains tools provided by %{oname}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

chmod 644 AUTHORS CREDITS ChangeLog Libraries.txt README.unix

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
export CFLAGS="%{optflags} -O3 -funroll-loops -ffast-math -fomit-frame-pointer -fexpensive-optimizations"
# using autogen.sh results in configure failing with a problem in
# ADD_CFLAGS, as of 0.7.3 - AdamW 2008/12
#autoreconf

%configure2_5x	\
	--enable-shared \
	--enable-static \
	--enable-IL \
	--enable-ILU \
	--enable-ILUT \
	%ifnarch ix86
	--enable-x86_64 \
	--enable-sse \
	--enable-sse2 \
	--disable-sse3 \
	%else
	--enable-x86 \
	--disable-x86_64
	--disable-sse \
	--disable-sse2 \
	--disable-sse3 \
	%endif
	--with-x \
	--with-zlib=yes \
	--enable-release

%make

%install
%__rm -rf %{buildroot}
%makeinstall_std

%clean
%__rm -rf %{buildroot}

%files -n %{libname}
%doc AUTHORS CREDITS ChangeLog Libraries.txt README.unix
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/IL
%{_infodir}/*.info.*

%files -n %{staticname}
%{_libdir}/*.a

%files utils
%{_bindir}/ilur
