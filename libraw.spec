#
# Conditional build:
%bcond_without	openmp	# OpenMP support
%bcond_without	gpl2	# GPL v2+ demosaic pack
%bcond_without	gpl3	# GPL v3+ demosaic pack
%bcond_without	zlib	# ZLIB for deflated DNG format support
#
%if %{without gpl2}
%undefine	gpl3
%endif
Summary:	LibRaw - a library for reading RAW files
Summary(pl.UTF-8):	LibRaw - biblioteka do odczytu plików RAW
Name:		libraw
Version:	0.18.13
%define	demosaic_ver	0.18.8
Release:	1
%if %{with gpl3}
License:	GPL v3+
%else
%if %{with gpl2}
License:	GPL v2+
%else
License:	LGPL v2.1 or CDDL v1.0
%endif
%endif
Group:		Libraries
#Source0Download: http://www.libraw.org/download#stable
Source0:	https://www.libraw.org/data/LibRaw-%{version}.tar.gz
# Source0-md5:	b7b65b3f05f4b4b570b07799b1a5a467
Source1:	https://www.libraw.org/data/LibRaw-demosaic-pack-GPL2-%{demosaic_ver}.tar.gz
# Source1-md5:	68b821b4a72054d0c0908e4d7b16fcfe
Source2:	https://www.libraw.org/data/LibRaw-demosaic-pack-GPL3-%{demosaic_ver}.tar.gz
# Source2-md5:	260cd142472027c8f7710a1a4edc9975
Patch0:		%{name}-zlib.patch
URL:		https://www.libraw.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_openmp:BuildRequires:	gcc >= 6:4.2}
BuildRequires:	jasper-devel
BuildRequires:	lcms2-devel >= 2
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libjpeg-devel >= 8
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
# zlib with pkgconfig support
%{?with_zlib:BuildRequires:	zlib-devel >= 1.2.3.3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part
of drawbacks have already been eliminated and part will be fixed in
future. The users of the library are provided with API to be built
into their software programs.

%description -l pl.UTF-8
LibRaw to biblioteka do odczytu plików RAW uzyskanych z cyfrowych
aparatów fotograficznych (w formacie CRW/CR2, NEF, RAF, DNG i innych).

LibRaw jest oparty na kodzie źródłowym dcraw, z którego część wad
została już wyeliminowana, a część zostanie poprawiona w przyszłości.

%package samples
Summary:	LibRaw sample programs
Summary(pl.UTF-8):	Programy przykładowe do LibRaw
Group:		Applications/Graphics

%description samples
LibRaw sample programs.

%description samples -l pl.UTF-8
Programy przykładowe do LibRaw.

%package devel
Summary:	Header files for LibRaw
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LibRaw
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	jasper-devel
Requires:	lcms2-devel >= 2
%{?with_openmp:Requires:	libgomp-devel}
Requires:	libjpeg-devel >= 8
Requires:	libstdc++-devel
%{?with_zlib:Requires:	zlib-devel >= 1.2.3.3}

%description devel
Header files for LibRaw.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibRaw.

%package static
Summary:	Static LibRaw library
Summary(pl.UTF-8):	Statyczna biblioteka LibRaw
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibRaw library.

%description static -l pl.UTF-8
Statyczna biblioteka LibRaw.

%prep
%setup -q -n LibRaw-%{version} %{?with_gpl2:-a1} %{?with_gpl3:-a2}
%patch0 -p1

%if %{with gpl2}
for f in LibRaw-demosaic-pack-GPL2-%{demosaic_ver}/{COPYRIGHT,Changelog,README} ; do
	cp -p $f $(basename $f).demosaic-pack-GPL2
done
%endif
%if %{with gpl3}
for f in LibRaw-demosaic-pack-GPL3-%{demosaic_ver}/{COPYRIGHT,Changelog,README} ; do
	cp -p $f $(basename $f).demosaic-pack-GPL3
done
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-demosaic-pack-gpl2=%{?with_gpl2:LibRaw-demosaic-pack-GPL2-%{demosaic_ver}}%{!?with_gpl2:no} \
	--enable-demosaic-pack-gpl3=%{?with_gpl3:LibRaw-demosaic-pack-GPL3-%{demosaic_ver}}%{!?with_gpl3:no} \
	%{!?with_openmp:--disable-openmp} \
	%{?with_zlib:--enable-zlib}

%{__make} \
	%{?with_openmp:lib_libraw_la_LIBADD=-lgomp lib_libraw_r_la_LIBADD=-lgomp}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libraw*.la

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT Changelog.txt README README.demosaic-packs %{?with_gpl2:*.demosaic-pack-GPL2} %{?with_gpl3:*.demosaic-pack-GPL3}
%attr(755,root,root) %{_libdir}/libraw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libraw.so.16
%attr(755,root,root) %{_libdir}/libraw_r.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libraw_r.so.16

%files samples
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/4channels
%attr(755,root,root) %{_bindir}/dcraw_emu
%attr(755,root,root) %{_bindir}/dcraw_half
%attr(755,root,root) %{_bindir}/half_mt
%attr(755,root,root) %{_bindir}/mem_image
%attr(755,root,root) %{_bindir}/multirender_test
%attr(755,root,root) %{_bindir}/postprocessing_benchmark
%attr(755,root,root) %{_bindir}/raw-identify
%attr(755,root,root) %{_bindir}/simple_dcraw
%attr(755,root,root) %{_bindir}/unprocessed_raw

%files devel
%defattr(644,root,root,755)
%doc doc/*.html
%attr(755,root,root) %{_libdir}/libraw.so
%attr(755,root,root) %{_libdir}/libraw_r.so
%{_includedir}/libraw
%{_pkgconfigdir}/libraw.pc
%{_pkgconfigdir}/libraw_r.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libraw.a
%{_libdir}/libraw_r.a
