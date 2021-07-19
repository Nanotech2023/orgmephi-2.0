import { Component, OnInit } from '@angular/core'
import { emptyParticipant, Gender, ParticipantRegister } from '@/users/models/participant'
import { ParticipantService } from '@/users/services/participant.service'
import { ValidationErrors } from '@angular/forms'


@Component( {
    selector: 'app-participant-registration-form',
    templateUrl: './participant-registration-form.component.html',
    styleUrls: [ './participant-registration-form.component.scss' ]
} )
export class ParticipantRegistrationFormComponent implements OnInit
{

    participant: ParticipantRegister
    genderOptions: Gender[] = [ Gender.male, Gender.female ]
    countriesList: string[] = []

    constructor( private service: ParticipantService )
    {
        this.participant = emptyParticipant
    }

    ngOnInit(): void
    {
        this.countriesList = this.service.getCountriesList()
    }
}
