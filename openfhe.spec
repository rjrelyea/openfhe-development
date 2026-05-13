%global major_vers 1
%global vers 1.5.1
Name:       {{{ git_dir_name }}}
Version:    {{{ git_dir_version lead=1.5.1 }}}
Release:    1%{?dist}
Summary:    OpenFHE - Open-Source Fully Homomorphic Encryption Library

License:    BSD 2-Clause License
URL:        https://openfhe-development.readthedocs.io
VCS:        {{{ git_dir_vcs }}}

Source: {{{ git_dir_pack }}}

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: make
#BuildRequires: ntl-devel
#BuildRequires: gmp-devel
#Requires: ntl
#Requires: gmp

%description
Fully Homomorphic Encryption (FHE) is a powerful cryptographic primitive
that enables performing computations over encrypted data without having
access to the secret key. OpenFHE is an open-source FHE library that
includes efficient implementations of all common FHE schemes:
    Brakerski/Fan-Vercauteren (BFV) scheme for integer arithmetic
    Brakerski-Gentry-Vaikuntanathan (BGV) scheme for integer arithmetic
    Cheon-Kim-Kim-Song (CKKS) scheme for real-number arithmetic 
        (includes approximate bootstrapping)
    Ducas-Micciancio (DM/FHEW), Chillotti-Gama-Georgieva-Izabachene
        (CGGI/TFHE), and Lee-Micciancio-Kim-Choi-Deryabin-Eom-Yoo
        (LMKCDEY) schemes for evaluating Boolean circuits and arbitrary
        functions over larger plaintext spaces using lookup tables
OpenFHE also supports hybrid vectorized schemes, with the goal of enabling
the FHEW/TFHE-like functional bootstrapping capability for schemes such as
CKKS and BFV. In particular, OpenFHE supports
    Switching between CKKS and FHEW/TFHE to evaluate non-smooth functions,
        e.g., comparison, using (scalar) FHEW/TFHE functional bootstrapping
    Switching between RLWE (a scheme equivalent to the coefficient-encoded
        additive BFV scheme) and CKKS to evaluate arbitrary lookup tables
        over vectors of integers, e.g., modular reduction, comparison or
        S-box, using vectorized functional bootstrapping implemented in CKKS
OpenFHE also supports partial schemes, called schemelets, such as RLWE which
is equivalent to the coefficient-encoded additive BFV scheme. In OpenFHE,
the RLWE schemelet is the starting point for the vectorized functional
bootstrapping capability, which allows the evaluation of arbitrary lookup
tables over vectors of integers, e.g., modular reduction, comparison or Sbox,
using CKKS in an intermediate step.

OpenFHE also includes the following multiparty extensions of FHE:
    Threshold FHE for BGV, BFV, and CKKS schemes
    Interactive bootstrapping for Threshold CKKS
    Proxy Re-Encryption for BGV, BFV, and CKKS schemes
OpenFHE supports any GNU C++ compiler version 9 or above and clang C++ compiler
version 10 or above. To achieve the best runtime performance, we recommend
following the guidelines outlined in building OpenFHE for best performance.


%prep
{{{ git_dir_setup_macro }}}

%build
CXFLAGS=$RPM_OPT_FLAGS
%if 0%{?fedora} > 43
 CXFLAGS="$CXFLAGS -Wno-error=array-bounds -Wno-error=cpp"
%endif
%if 0%{?fedora} >= 43
 CXFLAGS="$CXFLAGS -Wno-error=maybe-uninitialized -Wno-error=uninitialized"
%endif
echo "CXFLAGS=$CXFLAGS"
mkdir build
pushd build
#cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT/usr -DCMAKE_BUILD_TYPE=Debug -DBUILD_UNITTESTS=OFF -DBUILD_BENCHMARKS=OFF ..
cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT/usr -DCMAKE_CXX_FLAGS\:STRING="$CXFLAGS" -DBUILD_UNITTESTS=OFF -DBUILD_BENCHMARKS=OFF ..
make
popd

%install
pushd build
make install
popd

# sigh, the openfhe-devel cmake files hard-code 'lib', if wer aren't installing
# in lib, mv the lib directory there.
if [ ! -d $RPM_BUILD_ROOT/%{_libdir} ]; then
   mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT/%{_libdir}
fi

#don't package the cmake files (confuses RPM)
rm -rf $RPM_BUILD_ROOT/%{_libdir}/OpenFHE

%files
%{_libdir}/libOPENFHEbinfhe.so
%{_libdir}/libOPENFHEcore.so
%{_libdir}/libOPENFHEpke.so
%{_libdir}/libOPENFHEbinfhe.so.%{major_vers}
%{_libdir}/libOPENFHEcore.so.%{major_vers}
%{_libdir}/libOPENFHEpke.so.%{major_vers}
%{_libdir}/libOPENFHEbinfhe.so.%{vers}
%{_libdir}/libOPENFHEcore.so.%{vers}
%{_libdir}/libOPENFHEpke.so.%{vers}
%{_includedir}/openfhe/*

%check
pushd build
make clean
popd

%changelog
{{{ git_dir_changelog }}}
* Tue May 12 2026 Bob Relyea <rrelyea@redhat.com> - 0.0.0-0
- initial import from openfhe-devel gitlib
#EOF
