<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CreateFilmRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'title' => 'required|min:10|max:190',
            'description'  => 'required|min:10|max: 1000',
            'url'  => 'required|min:10|max: 190'
        ];
    }

    public function messages()
    {
        return [
            'title.required' => 'Proszę wypełnić pole <b>Tytuł</b>.',
            'title.min' => 'Za krótki <b>Tytuł</b>: wymagane co najmniej 10 znaków.',
            'title.max' => 'Za długi <b>Tytuł</b>: wymagane co najwyżej 190 znaków.',
            'description.required'  => 'Proszę wypełnić pole <b>Opis</b>.',
            'description.min' => 'Za krótki <b>Opis</b>: wymagane co najmniej 10 znaków.',
            'description.max' => 'Za długi <b>Opis</b>: wymagane co najwyżej 1000 znaków.',
            'url.required'  => 'Proszę wypełnić pole <b>URL</b>.',
            'url.min' => 'Za krótki <b>URL</b>: wymagane co najmniej 10 znaków.',
            'url.max' => 'Za długi <b>URL</b>: wymagane co najwyżej 190 znaków.'
        ];
    }

}
