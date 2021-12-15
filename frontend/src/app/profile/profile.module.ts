import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ReactiveFormsModule } from '@angular/forms'
import { PhoneValidatorDirective } from '@/shared/phone.validator.directive'
import { NgSelectModule } from '@ng-select/ng-select'
import { PasswordValidatorDirective } from '@/shared/password-validator.directive'
import { RouterModule } from '@angular/router'
import { PROFILE_COMPONENTS, PROFILE_ROUTES } from '@/profile/profile.module.components'


@NgModule( {
    declarations: [
        PROFILE_COMPONENTS,
        PhoneValidatorDirective,
        PasswordValidatorDirective
    ],
    exports: [
        PasswordValidatorDirective
    ],
    imports: [
        SharedModule,
        ReactiveFormsModule,
        NgSelectModule,
        RouterModule.forChild( PROFILE_ROUTES )
    ]
} )
export class ProfileModule {}
