import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'


@Injectable( {
    providedIn: 'root'
} )
export class ParticipantService
{
    regions = [ 'Москва', 'Санкт-Петербург' ]

    constructor( private http: HttpClient )
    {
    }

    //TODO observable
    getCountriesList(): string[]
    {
        return [ "Россия", "Беларусь" ]
    }

    getRegions( name: string )
    {
        if ( !name || !name?.length )
            return []

        return this.regions.filter( item => item.toLocaleLowerCase().includes( name.toLocaleLowerCase() ) )
    }
}