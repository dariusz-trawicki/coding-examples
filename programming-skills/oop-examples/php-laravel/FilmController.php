<?php

namespace App\Http\Controllers;

use App\Models\Film;
use App\Models\Category;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Http\Requests\CreateFilmRequest;

class FilmController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth', ['except' => ['index', 'show']]);
    }


    public function index()
    {
        $films = Film::orderBy('title', 'asc')->paginate(9);
        $title = 'Filmy polecane z Youtube';

        return view('films.index', compact('films', 'title'));
    }


    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Film  $film
     * @return \Illuminate\Http\Response
     */
    public function show(Film $film)
    {
        $title = 'ogłoszenia';
        $numberOfCategories = 3;
        $PopCategories = Category::withCount('films')->latest('films_count')->take($numberOfCategories)->with('films')->get();
        $PopCategories->transform(function($category, $numberOfCategories) {
            $topFilms = $category->films->take($numberOfCategories);
            unset($category->films);
            $category->films = $topFilms;
            return $category;
        });
        $filmCount = Film::count();
        $categoryCount = Category::count();

        return view('films.show', compact('title','film', 'PopCategories', 'filmCount', 'categoryCount'));

    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        $title = 'nowy film polecany z Youtube';
        $categories = Category::pluck('name','id');

        return view('films.create', compact('title', 'categories'));
    }


    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\CreateFilmRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(CreateFilmRequest $request)
    {
        $film = new Film($request->all());
        $film->save();
        $film->categories()->sync($request->input('CategoryList'));

        return redirect()->route('filmy.index')->with('success', 'Nowy film został zapisany.');
    }


    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\Film  $film
     * @return \Illuminate\Http\Response
     */
    public function edit(Film $film)
    {
        $title = 'edycja filmu z Youtube';
        $categories = Category::pluck('name','id');

        return view('films.edit', compact('title', 'film', 'categories'));
    }


    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\CreateFilmRequest  $request
     * @param  \App\Models\Film  $film
     * @return \Illuminate\Http\Response
     */
    public function update(CreateFilmRequest $request, Film  $film)
    {
        $film->update($request->all());
        $film->categories()->sync($request->input('CategoryList'));

        return redirect()->route('filmy.index')->with('success', 'Film został zaktualizowany.');
    }

    /**
     * (SOFT) Delete the specified resource from storage.
     *
     * @param  \App\Models\Film  $film
     * @return \Illuminate\Http\Response
     */
    public function destroy(Film  $film)
    {
        $film->delete();
        return redirect()->route('filmy.index')
                            ->with('success','Wybrany film został usunięty.');
    }
}
