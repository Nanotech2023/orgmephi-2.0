import { NgModule } from '@angular/core'
import { HeaderComponent } from '@/layout/header/header.component'
import { FooterComponent } from '@/layout/footer/footer.component'
import { SharedModule } from '@/shared/shared.module'
import { ConfirmAccountComponent } from '@/layout/confirm-account/confirm-account.component'


const COMPONENTS = [
    HeaderComponent,
    FooterComponent,
    ConfirmAccountComponent
]


@NgModule( {
    declarations: COMPONENTS,
    exports: COMPONENTS,
    imports: [
        SharedModule
    ]
} )
export class LayoutModule {}