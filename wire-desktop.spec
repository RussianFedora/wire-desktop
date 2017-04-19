%global __provides_exclude_from %{_libdir}/%{name}/.*\\.so
%global privlibs libffmpeg
%global __requires_exclude ^(%{privlibs})\\.so

# Oh, it fetch some binaries. Fucking nodejs
%global debug_package %{nil}

Summary:	Modern communication, full privacy
Name:		wire-desktop
Version:	2.13.2739
Release:	1%{?dist}

License:	GPLv3
URL:		https://wire.com
Source0:	https://github.com/wireapp/%{name}/archive/release/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop

BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	git
BuildRequires:	hicolor-icon-theme
BuildRequires:	npm >= 3.10.0

%if 0%{?fedora} >= 25
BuildRequires:	python2
%endif

%description
Wire is an open source, cross-platform, encrypted instant messaging client. It
uses the Internet to make voice and video calls; send text messages, files,
images, videos, audio files and user drawings depending on the clients used. It
can be used on any of the available clients, requiring a phone number or email
for registration.

%prep
%autosetup -n %{name}-release-%{version}

%build
# Oh, NodeJS
npm install
node_modules/.bin/build --linux tar.xz

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -r wrap/dist/linux*unpacked/* \
	%{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_bindir}
for size in 16 24 32 48 64 96 128 256; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
    install -m644 node_modules/electron-builder/templates/linux/electron-icons/${size}x${size}.png \
	%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

cd %{buildroot}%{_bindir}
ln -s ../%{_lib}/%{name}/wire-desktop
cd -

%post
update-desktop-database &> /dev/null || :
touch --no-create /usr/share/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache --quiet /usr/share/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create /usr/share/icons/hicolor &>/dev/null
    gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed Apr 19 2017 Arkady L. Shane <ashejn@russianfedora.pro> - 2.13.2739-1
- initial build
