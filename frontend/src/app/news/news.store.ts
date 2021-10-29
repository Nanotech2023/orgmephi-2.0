import { Injectable } from '@angular/core'
import { ComponentStore } from '@ngrx/component-store'


export interface NewsState {}

const initialState: NewsState = {}


@Injectable()
export class NewsStore extends ComponentStore<NewsState>
{
    constructor()
    {
        super( initialState )
    }
}
