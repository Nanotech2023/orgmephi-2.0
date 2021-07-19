import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'


@Injectable( {
    providedIn: 'root'
} )
export class ParticipantService
{
    constructor( private http: HttpClient )
    {
    }

    //TODO observable
    getCountriesList(): string[]
    {
        return [ "Россия", "Белорусь" ]
    }
}