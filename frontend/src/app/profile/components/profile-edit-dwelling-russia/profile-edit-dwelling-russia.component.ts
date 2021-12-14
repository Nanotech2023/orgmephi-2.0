import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { City, Location, LocationRussia, LocationRussiaCity, LocationTypeEnum, Region } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'


@Component( {
    selector: 'app-profile-edit-dwelling-russia',
    templateUrl: './profile-edit-dwelling-russia.component.html',
    styleUrls: [ './profile-edit-dwelling-russia.component.scss' ]
} )
export class ProfileEditDwellingRussiaComponent implements OnInit
{
    @Input() model!: Location
    @Input() city!: LocationRussiaCity
    @Output() modelChange = new EventEmitter<Location>()
    @Output() cityChange = new EventEmitter<LocationRussiaCity>()
    regions$!: Observable<Region[]>
    cities$!: Observable<City[]>

    constructor( private usersService: UsersService )
    {
    }

    ngOnInit(): void
    {
        this.regions$ = this.usersService.userRegistrationInfoRegionsGet().pipe( map( item => item.region_list.filter( x => x.name !== "Некорректные данные" && x.name !== "Онлайн" ) ) )
    }

    getEmptyLocation(): LocationRussia
    {
        return {
            location_type: LocationTypeEnum.Russian,
            country: "Россия",
            city: { region_name: "", name: "" },
            rural: false
        }
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }

    onRegionChange(): void
    {
        this.city.name = ""
        this.cityChange.emit( this.city )
        this.onModelChange()
        this.cities$ = this.usersService.userRegistrationInfoCitiesRegionGet( this.city.region_name ).pipe( map( item => item.city_list ) )
    }

    onCityChange(): void
    {
        this.cityChange.emit( this.city )
        this.onModelChange()
    }
}
