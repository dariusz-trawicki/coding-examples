<nav class="bg-white dark:bg-gray-900 fixed w-full z-50 top-0 left-0 border-b border-gray-200
            dark:border-gray-600">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <div>
            <a href="{{route('start')}}" class="flex items-center">
                <img src="{{ asset('img/logo_el.png') }}" class="h-8 mr-3" alt="Logo">
            </a>
        </div>
        <div class="flex md:order-2">
            <button data-collapse-toggle="navbar-dropdown" type="button" class="md:hidden inline-flex items-center
                p-2 w-20 h-10 justify-center text-sm text-gray-500 border border-gray-200 rounded-lg
                focus:outline-none focus:ring-2 focus:ring-gray-100 active:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700
                dark:focus:ring-gray-600" aria-controls="navbar-search" aria-expanded="false">
                <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                </svg>
                <svg class="w-5 h-5 ml-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
                </svg>
                <span class="sr-only">Szukaj produktu</span>
            </button>
        </div>

        {{--form "Szukaj" for mobile --}}
        <div class="hidden w-full md:block md:w-auto" id="navbar-dropdown">
            <div class="mt-3 md:hidden">
                <div class="relative ">
                    <form method="GET" id="searching-form" action="{{ route('produkty.index') }}"
                          class="mb-4 items-center space-x-2 ">
                        <div class="mb-4 flex w-full items-center">
                            <div class="w-full">
                                <div class="relative">
                                    <button type="button" class="absolute top-0 left-0 flex h-full items-center pl-2"
                                            onclick="document.getElementById('searching-form').submit();">
                                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                                        </svg>
                                    </button>
                                    <input type="text" placeholder="Szukaj produktu..."
                                           name="s" value="{{ request('s') }}" id="search"
                                           class="w-full rounded-md border-0 py-2 px-2.5 pl-10 pr-8 text-sm ring-1 ring-slate-300 placeholder:text-slate-400 focus:ring-2" />
                                    <button type="button" class="absolute top-0 right-0 flex h-full items-center pr-2"
                                            onclick="document.getElementById('search').value = '';">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                             stroke="currentColor" class="h-4 w-4 text-slate-500">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <x-submit_btn class="ml-4">Szukaj</x-submit_btn>
                        </div>
                    </form>
                </div>
            </div>
            <ul class="flex flex-col p-4 md:p-0 mt-4 text-[18px] border
                border-gray-100 rounded-lg font-cg
                bg-white md:flex-row md:space-x-8 md:mt-0 md:border-0 md:bg-transparent dark:bg-gray-800
                md:dark:bg-gray-900 dark:border-gray-700">
                <li>
                    <a href="{{  route('start') }}" class="block py-2 pl-3 pr-4
                          md:p-0 dark:text-gray-100 hover:text-gold active:bg-normal-50 focus:bg-normal-50 md:dark:hover:text-blue-500 dark:hover:bg-gray-700
                          dark:hover:text-white md:dark:hover:bg-transparent">
                        <span class="link link-underline link-underline-black underline-offset-8">START</span>
                    </a>
                </li>
                <li>
                    <a href="{{  route('onas') }}" class="block py-2 pl-3 pr-4
                          md:p-0 dark:text-white hover:text-gold active:bg-normal-50 focus:bg-normal-50 md:dark:hover:text-blue-500 dark:hover:bg-gray-700
                          font-display dark:hover:text-white md:dark:hover:bg-transparent">
                        <span class="link link-underline link-underline-black">O NAS</span>
                    </a>
                </li>
                <li>
                    <!-- Dropdown menu -->
                    <button id="dropdownNavbarLink" data-dropdown-toggle="dropdownNavbar" data-dropdown-trigger="hover"md-se
                            class="flex items-center justify-between w-full py-2 pl-3
                                pr-4 rounded hover:text-gold active:bg-normal-50 focus:bg-normal-50 hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:white
                                md:p-0 md:w-auto dark:text-white md:dark:hover:text-blue-500 dark:focus:text-white
                                dark:border-gray-700 dark:hover:bg-gray-700 md:dark:hover:bg-transparent
                              block py-2 pl-3 pr-4
                              md:p-0 dark:text-white md:dark:hover:text-WHITE dark:hover:bg-gray-700
                              font-display
                            dark:hover:text-white md:dark:hover:bg-transparent">
                        <span class="link link-underline link-underline-black">OFERTA</span>
                        <svg class="w-2.5 h-2.5 ml-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                        </svg>
                    </button>
                    <div id="dropdownNavbar" class="z-10 hidden font-normal bg-white divide-y divide-gray-100
                    rounded-lg shadow w-56 dark:bg-gray-700 dark:divide-gray-600">
                        <ul class="py-2 text-[15px] text-black dark:text-gray-400" aria-labelledby="dropdownLargeButton">
                            <li>
                                <a href="{{  route('wyroby_piekarnicze') }}" class="block px-4 py-2
                                        hover:text-gold active:bg-normal-50 focus:bg-normal-50 hover:bg-neutral-50 dark:hover:bg-gray-600
                                        dark:hover:text-white">
                                    <span class="link link-underline link-underline-black">WYROBY PIEKARNICZE</span></a>
                            </li>
                            <li>
                                <a href="{{  route('kategorie.show', 6) }}" class="block px-4 py-2
                                        hover:text-gold active:bg-normal-50 focus:bg-normal-50 hover:bg-neutral-50 dark:hover:bg-gray-600
                                        dark:hover:text-white">
                                    <span class="link link-underline link-underline-black"> WYROBY PÓŁCUKIERNICZE</span>
                                </a>
                            </li>
                            <li>
                                <a href="{{  route('wyroby_cukiernicze') }}" class="block px-4 py-2
                                        hover:text-gold active:bg-normal-50 focus:bg-normal-50 hover:bg-neutral-50 dark:hover:bg-gray-600 dark:hover:text-white">
                                    <span class="link link-underline link-underline-black"> WYROBY CUKIERNICZE</span>
                                </a>
                            </li>
                        </ul>
                        <div class="py-1  text-[15px] dark:hover:bg-gray-600 dark:text-gray-400 dark:hover:text-white">
                            <a href="{{  route('wyroby_inne') }}" class="block px-4 py-2
                                    hover:text-gold active:bg-normal-50 focus:bg-normal-50
                                    hover:bg-neutral-50 dark:hover:bg-gray-600 dark:hover:text-white">
                                <span class="link link-underline link-underline-black">WYROBY INNE</span></a>
                        </div>
                    </div>
                </li>
                <li>
                    <a href="{{  route('sklepy') }}" class="block py-2 pl-3 pr-4
                        md:p-0 dark:text-white hover:text-gold active:bg-normal-50 focus:bg-normal-50 md:dark:hover:text-blue-500 dark:hover:bg-gray-700
                        font-display dark:hover:text-white md:dark:hover:bg-transparent">
                        <span class="link link-underline link-underline-black">SKLEPY</span>
                    </a>
                </li>
                <li>
                    <a href="{{  route('aktualnosci.index') }}" class="block py-2 pl-3 pr-4
                          md:p-0 dark:text-white hover:text-gold active:bg-normal-50 focus:bg-normal-50 md:dark:hover:text-blue-500 dark:hover:bg-gray-700
                          font-display dark:hover:text-white md:dark:hover:bg-transparent">
                        <span class="link link-underline link-underline-black">AKTUALNOŚCI</span></a>
                </li>
                <li>
                    <a href="{{  route('kontakt') }}" class="block py-2 pl-3 pr-4
                        md:p-0 dark:text-white hover:text-gold active:bg-normal-50 focus:bg-normal-50 md:dark:hover:text-blue-500 dark:hover:bg-gray-700
                        font-display dark:hover:text-white md:dark:hover:bg-transparent">
                        <span class="link link-underline link-underline-black">KONTAKT</span>
                    </a>
                </li>
            </ul>
        </div>

        {{--From "search" for >= lg --}}
        <div class="relative hidden lg:block ml-32 -mr-16">
            <form method="GET" id="lg-searching-form" action="{{ route('produkty.index') }}"
                  class="items-center md:ml-4">
                {{--@csrf--}}
                <div class="relative">
                    <button type="button" class="absolute top-0 left-0 flex h-full items-center pl-2"
                            onclick="document.getElementById('lg-searching-form').submit();">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                        </svg>
                    </button>
                    <input type="text" placeholder="Szukaj produktu..."
                           name="s" value="{{ request('s') }}" id="lg-search"
                           class="w-full rounded-md border-0 py-2 px-2.5 pl-10 pr-8 text-sm  md:text-base ring-1
                           ring-slate-300 placeholder:text-slate-400 focus:ring-1 focus:ring-slate-500" />
                    <button type="button" class="absolute top-0 right-0 flex h-full items-center pr-2"
                            onclick="document.getElementById('lg-search').value = '';">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                             stroke="currentColor" class="h-4 w-4 text-slate-500">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </form>
        </div>
    </div>
</nav>