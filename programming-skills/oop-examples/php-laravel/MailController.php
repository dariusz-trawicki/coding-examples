<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use App\Mail\SendMail;
use Exception;

class MailController extends Controller
{
    function sendmail(Request $request)
    {
        $rules = [
            'name' => 'required|min:2|max:200',
            'message' => 'required|min:10|max:1000',
            'captcha' => 'required|captcha',
        ];

        if ($request->filled('email')) {
            $rules['email'] = 'email';
        }

        $request->validate($rules);

        $data = $request->only(['name', 'message']);
        if ($request->filled('email')) {
            $data['email'] = $request->email;
        }

        try {
            Mail::to('xxx@yyy.pl')->send(new SendMail($data));
            return back()->with('email_succes', true);
        } catch (Exception $e) {
            return back()->with('email_succes', false);
        }
    }

    public function reloadCaptcha()
    {
        return response()->json(['captcha'=> captcha_img()]);
    }
}
