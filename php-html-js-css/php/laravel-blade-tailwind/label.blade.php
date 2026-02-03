<label class="block mb-1 text-base font-medium text-gray-900 dark:text-white"
       for="{{ $for }}">
    {{ $slot }} @if($required)<span>(*)</span>@endif
</label>