import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { map } from 'rxjs/operators'
import { UsersService } from '@api/users/users.service'
import { Observable } from 'rxjs'
import { LocationOther } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-dwelling-other',
    templateUrl: './profile-edit-dwelling-other.component.html',
    styleUrls: [ './profile-edit-dwelling-other.component.scss' ]
} )
export class ProfileEditDwellingOtherComponent implements OnInit
{
    @Input() model!: any
    @Input() country!: string
    @Output() modelChange = new EventEmitter<any>()
    @Output() countryChange: EventEmitter<string> = new EventEmitter<string>()
    countries$!: Observable<string[]>

    constructor( private usersService: UsersService )
    {
    }

    ngOnInit(): void
    {
        this.countries$ = this.usersService.userRegistrationInfoCountriesGet().pipe( map( item => item.country_list.map( x => x.name ) ) )
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }

    onCountryChange()
    {
        this.model.country = this.country
        this.countryChange.emit( this.country )
        this.onModelChange()
    }
}
