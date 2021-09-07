import { Component, EventEmitter, Input, Output } from '@angular/core'


@Component( {
    selector: 'app-participant-registration-form-education',
    templateUrl: './participant-registration-form-education.component.html',
    styleUrls: [ './participant-registration-form-education.component.scss' ]
} )
export class ParticipantRegistrationFormEducationComponent
{
    // @ts-ignore
    @Input() participant: ParticipantRegister
    @Output() participantChange: EventEmitter<ParticipantRegister> = new EventEmitter<ParticipantRegister>()

    filteredRegions: string[] = []
    filteredCities: string[] = []
    showRegionSuggest: boolean = false
    showCitySuggest: boolean = false
    educationTypes = Object.values( SchoolType )
    classes = [ ...Array( 7 ) ].map( ( _, index ) => 5 + index )

    constructor( private service: ParticipantService ) { }

    getFilteredRegions()
    {
        this.filteredRegions = this.service.getRegions( this.participant.education.region )
        this.showRegionSuggest = !!this.filteredRegions?.length
    }

    getFilteredCities()
    {
        this.filteredCities = this.service.getRegions( this.participant.education.city )
        this.showCitySuggest = !!this.filteredCities?.length
    }

    setRegion( region: string )
    {
        this.participant.education.region = region
        this.showRegionSuggest = false
    }

    setCity( city: string )
    {
        this.participant.education.city = city
        this.showCitySuggest = false
    }
}
