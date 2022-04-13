import { NgModule } from '@angular/core'
import { SharedModule } from '@/shared/shared.module'
import { ReactiveFormsModule } from '@angular/forms'
import { NgSelectModule } from '@ng-select/ng-select'
import { RouterModule } from '@angular/router'
import { PROFILE_COMPONENTS, PROFILE_ROUTES } from '@/profile/profile.module.components'


@NgModule( {
    declarations: [
        PROFILE_COMPONENTS,
    ],
    imports: [
        SharedModule,
        ReactiveFormsModule,
        NgSelectModule,
        RouterModule.forChild( PROFILE_ROUTES )
    ]
} )
export class ProfileModule {}
